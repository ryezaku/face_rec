from enum import Enum


class DocStatus(Enum):
    FRONT_DOC_CAMERA_GRAYSCALE = "FRONT_DOC_CAMERA_GRAYSCALE"
    BACK_DOC_CAMERA_GRAYSCALE = "BACK_DOC_CAMERA_GRAYSCALE"
    FRONT_DOC_GRAYSCALE = "A black and white photocopy"
    BACK_DOC_GRAYSCALE = "A black and white photocopy "
    PUNCHED_DOCUMENT = "When a document has been invalidated"
    GOOD = "GOOD"
    NO_DOCUMENT = "No document found"
    FRONT_DOC_BAD_QUALITY = "Blurry"
    BACK_DOC_BAD_QUALITY =  "Blurry"
    DIGITAL_COPY = "The document displays on an electronic device (i.e. taking a photo of an ID on the computer from a mobile phone)"


