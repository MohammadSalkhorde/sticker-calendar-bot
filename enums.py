class UserState:
    START = "START"
    WAITING_NAME = "WAITING_NAME"           # جدید: انتظار برای نام
    WAITING_ID_STENCIL = "WAITING_ID_STENCIL" # جدید: انتظار برای آیدی
    WAITING_RECEIPT = "WAITING_RECEIPT"
    WAITING_ADMIN = "WAITING_ADMIN"
    WAITING_FOR_BROADCAST = "WAITING_FOR_BROADCAST"
    WAITING_APPROVAL = "WAITING_APPROVAL" # برای مرحله بعد از ارسال فیش