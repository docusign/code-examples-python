from os import path
import re

demo_docs_path = path.abspath(path.join(path.dirname(path.realpath(__file__)), "static/demo_documents"))

# Pattern for validating signer name and email
pattern = re.compile("([^\w \-\@\.\,])+")

signer_client_id = 1000  # Used to indicate that the signer will use embedded
# signing. Represents the signer"s userId within
# your application.

authentication_method = "None"  # How is this application authenticating

minimum_buffer_min = 3

# Template name for create template example
template_name = "Example Signer and CC template"

# Name of static doc file
doc_file = "World_Wide_Corp_fields.pdf"
# Name of static pdf file
pdf_file = "World_Wide_Corp_lorem.pdf"

# Base uri for callback function
base_uri_suffix = "/restapi"


# Default languages for brand
languages = {
    "Arabic": "ar",
    "Armenian": "hy",
    "Bahasa Indonesia": "id",
    "Bahasa Malay": "ms",
    "Bulgarian": "bg",
    "Chinese Simplified": "zh_CN",
    "Chinese Traditional": "zh_TW",
    "Croatian": "hr",
    "Czech": "cs",
    "Danish": "da",
    "Dutch": "nl",
    "English UK": "en_GB",
    "English US": "en",
    "Estonian": "et",
    "Farsi": "fa",
    "Finnish": "fi",
    "French": "fr",
    "French Canada": "fr_CA",
    "German": "de",
    "Greek": "el",
    "Hebrew": "he",
    "Hindi": "hi",
    "Hungarian": "hu",
    "Italian": "it",
    "Japanese": "ja",
    "Korean": "ko",
    "Latvian": "lv",
    "Lithuanian": "lt",
    "Norwegian": "no",
    "Polish": "pl",
    "Portuguese": "pt",
    "Portuguese Brasil": "pt_BR",
    "Romanian": "ro",
    "Russian": "ru",
    "Serbian": "sr",
    "Slovak": "sk",
    "Slovenian": "sl",
    "Spanish": "es",
    "Spanish Latin America": "es_MX",
    "Swedish": "sv",
    "Thai": "th",
    "Turkish": "tr",
    "Ukrainian": "uk",
    "Vietnamese": "vi"
}

# Default settings for updating and creating permissions
settings = {
    "useNewDocuSignExperienceInterface": "optional",
    "allowBulkSending": "true",
    "allowEnvelopeSending": "true",
    "allowSignerAttachments": "true",
    "allowTaggingInSendAndCorrect": "true",
    "allowWetSigningOverride": "true",
    "allowedAddressBookAccess": "personalAndShared",
    "allowedTemplateAccess": "share",
    "enableRecipientViewingNotifications": "true",
    "enableSequentialSigningInterface": "true",
    "receiveCompletedSelfSignedDocumentsAsEmailLinks": "false",
    "signingUiVersion": "v2",
    "useNewSendingInterface": "true",
    "allowApiAccess": "true",
    "allowApiAccessToAccount": "true",
    "allowApiSendingOnBehalfOfOthers": "true",
    "allowApiSequentialSigning": "true",
    "enableApiRequestLogging": "true",
    "allowDocuSignDesktopClient": "false",
    "allowSendersToSetRecipientEmailLanguage": "true",
    "allowVaulting": "false",
    "allowedToBeEnvelopeTransferRecipient": "true",
    "enableTransactionPointIntegration": "false",
    "powerFormRole": "admin",
    "vaultingMode": "none"
}

