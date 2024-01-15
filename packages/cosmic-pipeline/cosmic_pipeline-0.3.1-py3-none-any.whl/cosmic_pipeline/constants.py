from django.db import models


class OperandChoices(models.TextChoices):
    NONE = "none", "Equals"
    EXACT = "exact", "Exact"
    IEXACT = "iexact", "Exact (case-insensitive)"
    GT = "gt", "Greater than"
    GTE = "gte", "Greater than or equal to"
    LT = "lt", "Less than"
    LTE = "lte", "Less than or equal to"
    IN = "in", "In"
    ISNULL = "isnull", "Is null"


class AnnotateChoices(models.TextChoices):
    SUM = "sum", "Sum"
    AVG = "avg", "Average"
    MAX = "max", "Maximum"
    MIN = "min", "Minimum"
    COUNT = "count", "Count"

class QueryOperatorChoices(models.TextChoices):
    AND = "and", "And"
    OR = "or", "Or"
    NOT = "not", "Not"

class PostChangeProcessorChoices(models.TextChoices):
    SEND_EMAIL = "send_email", "Send Email"
    SEND_SMS = "send_sms", "Send SMS"
    SEND_SMS_EMAIL = "send_sms_email", "Send SMS and Email"