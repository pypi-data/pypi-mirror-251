import json
import random

from database_mysql_local.generic_crud import GenericCRUD
from logger_local.LoggerLocal import LoggerLocal
from variable_local.template import ReplaceFieldsWithValues

from .MessageChannels import MessageChannels
from .MessageConstants import object_message
from .MessageTemplates import MessageTemplates
from .Recipient import Recipient

VERSION = "20240116"

logger = LoggerLocal.create_logger(object=object_message)


class CompoundMessage(GenericCRUD):
    def __init__(self, message_id: int = None):
        GenericCRUD.__init__(self, default_schema_name="campaign", default_table_name="campaign_table",
                             default_view_table_name="campaign_view", default_id_column_name="campaign_id")
        self.message_template = MessageTemplates()
        self.message_id = message_id

    @staticmethod
    def get_unified_json(data: dict, version: str = VERSION):
        # TODO: move to sdk?
        return {"version": version, "data": data}

    def get_compound_message_after_text_template(self, campaign_id: int,
                                                 body: str = None, subject: str = None,
                                                 to_recipients: list[Recipient] = None) -> dict:
        """At this point we do not know the right channel. That is what we are trying to determine here."""
        logger.start()

        compound_message = {"DEFAULT": {},
                "WEB": {},
                "EMAIL": {},
                "SMS": {},
                "WHATSAPP": {}
                }

        channels_mapping = {
            MessageChannels.SMS.name: {"body": "sms_body_template", "subject": None},
            MessageChannels.EMAIL.name: {"body": "email_body_html_template", "subject": "email_subject_template"},
            MessageChannels.WHATSAPP.name: {"body": "whatsapp_body_template", "subject": None},
            "DEFAULT": {"body": "default_body_template", "subject": "default_subject_template"},
        }

        if body:
            textblocks_and_attributes = [{}]  # one textblock
            for message_channel, template_header in channels_mapping.items():
                textblocks_and_attributes[0][template_header["body"]] = body
                textblocks_and_attributes[0][template_header["subject"]] = subject
            criteria_json = {}  # TODO what should it be in case of body is given?

        else:  # If body is not given, get it from the database
            textblocks_and_attributes = self.message_template.get_textblocks_and_attributes()
            message_template_ids = super().select_multi_tuple_by_id(view_table_name="campaign_view",
                                                                    id_column_name="campaign_id",
                                                                    id_column_value=campaign_id,
                                                                    select_clause_value="message_template_id")
            message_template_ids = [message_template_id[0] for message_template_id in message_template_ids]
            criteria_json = self.message_template.get_critiria_json(
                message_template_id=random.choice(message_template_ids))
        logger.info({"textblocks_and_attributes": textblocks_and_attributes})

        for message_template_textblock_and_attributes in textblocks_and_attributes:
            for message_channel, template_header in channels_mapping.items():
                for part in ("body", "subject"):
                    compound_message[message_channel][f"{part}Blocks"] = {
                        "blockId": message_template_textblock_and_attributes.get("blockId"),
                        "blockTypeId": message_template_textblock_and_attributes.get("blockTypeId"),
                        "blockTypeName": message_template_textblock_and_attributes.get("blockTypeName"),
                        "questionId": message_template_textblock_and_attributes.get("questionId"),
                        "questionTypeId": message_template_textblock_and_attributes.get("questionTypeId"),
                        "questionTitle": message_template_textblock_and_attributes.get("questionTitle"),
                        "questionTypeName": message_template_textblock_and_attributes.get("questionTypeName"),
                        "profileBlocks": []
                    }
                    templates = [x for x in (message_template_textblock_and_attributes.get(template_header[part]),
                                             message_template_textblock_and_attributes.get("questionTitle"))
                                 if x]

                    message_template = " ".join(templates)
                    if not message_template:
                        logger.warning("message_template is empty", object={
                            "message_template_textblock_and_attributes": message_template_textblock_and_attributes})
                        continue
                    for recipient in (to_recipients or []):
                        preferred_lang_code = self.message_template.profile_local.get_preferred_lang_code_by_profile_id(
                            recipient.get_profile_id())
                        if (self.message_template.is_critiria_id_match_profile_id(
                                criteria_json, recipient.get_profile_id())
                                and preferred_lang_code == message_template_textblock_and_attributes.get("langCode")):
                            compound_message[message_channel][f"{part}Blocks"]["profileBlocks"].append(
                                # each profile has its own template, because of the language
                                {"profileId": recipient.get_profile_id(),
                                 "template": message_template,
                                 "processedTemplate": self._process_text_block(message_template, recipient=recipient),
                                 })

        # save in message table
        if self.message_id:
            super().set_schema(schema_name="message")
            super().update_by_id(
                table_name="message_table", id_column_name="message_id", id_column_value=self.message_id,
                data_json={"compound_message": json.dumps(compound_message)})
        logger.end(object={"compound_message": compound_message})
        return compound_message

    def _process_text_block(self, text_block_body: str, recipient: Recipient) -> str:
        template = ReplaceFieldsWithValues(message=text_block_body,
                                           language=recipient.get_preferred_language(),
                                           variable=recipient.variable_local)
        # TODO: get the sender name
        processed_text_block = template.get_variable_values_and_chosen_option(
            profile_id=recipient.get_profile_id(), kwargs={"target name": recipient.get_person_id(),  # TODO ?
                                                           "message_id": self.message_id})
        return processed_text_block
