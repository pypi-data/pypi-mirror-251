URL_SANDBOX = "https://sandboxapi.finnotech.ir"
URL_MAINNET = "https://apibeta.finnotech.ir"

BANK_AYANDEH = "062"
BANK_DEY = "066"
BANK_IRANZAMIN = "069"
BANK_EGHTESADENOVIN = "055"
BANK_ANSAR = "063"

GENDER_MALE = "مرد"
GENDER_FEMALE = "زن"

SCOPE_OAK_WITHDRAWAL_FROM_EXECUTE = "oak_withdrawal-from:execute"
SCOPE_OAK_TRANSFER_TO_EXECUTE = "oak_transfer-to:execute"
SCOPE_OAK_INQUIRY_TRANSFER_GET = "oak_inquiry-transfer:get"
SCOPE_OAK_PAYAS_GET = "oak_payas:get"
SCOPE_OAK_STATEMENT_GET = "oak_statement:get"
SCOPE_OAK_BALANCE_GET = "oak_balance:get"
SCOPE_OAK_USER_GET = "oak_user:get"
SCOPE_OAK_DEPOSITS_GET = "oak_deposits:get"
SCOPE_OAK_UNBLOCK_TRANSFER_INQUIRY_GET = "oak_unblock-transfer-inquiry:get"
SCOPE_OAK_BLOCK_ = "oak_block:*"
SCOPE_OAK_CHEQUE_ = "oak_cheque:*"
SCOPE_OAK_CARD_CHARGE_EXECUTE = "oak_card-charge:execute"
SCOPE_OAK_CARD_CHARGE_INQUIRY_GET = "oak:card-charge-inquiry:get"
SCOPE_OAK_VALID_CARD_GET = "oak:valid-card:get"
SCOPE_OAK_BILL_ACCOUNT_EXECUTE = "oak_bill-account:execute"
SCOPE_KILID_REQUESTS_GET = "kilid:requests:get"
SCOPE_KILID_REQUEST_CREATE = "kilid:request:create"
SCOPE_KILID_REQUEST_GET = "kilid:request:get"
SCOPE_KILID_REQUEST_DELETE = "kilid:request:delete"
SCOPE_KILID_REQUEST_UPDATE = "kilid:request:update"
SCOPE_CREDIT_SMS_BACK_CHEQUES_GET = "credit:sms-back-cheques:get"
SCOPE_CREDIT_SMS_FACILITY_INQUIRY_GET = "credit:sms-facility-inquiry:get"
SCOPE_ECITY_CC_POSTAL_CODE_INQUIRY = "ecity:cc-postal-code-inquiry:get"

SCOPE_OAK_IBAN_INQUIRY_GET = "oak:iban-inquiry:get"
SCOPE_CARD_INFORMATION_GET = "card:information:get"
SCOPE_CARD_LIST_GET = "card:list:get"
SCOPE_FACILITY_SHAHKAR_GET = "facility:shahkar:get"
SCOPE_FACILITY_CARD_TO_IBAN_GET = "facility:card-to-iban:get"
SCOPE_FACILITY_SMS_NID_VERIFICATION_GET = "facility:sms-nid-verification:get"
SCOPE_FACILITY_DEPOSIT_OWNER_VERIFICATION_GET = (
    "facility:deposit-owner-verification:get"
)
SCOPE_FACILITY_CC_BANK_INFO_GET = "facility:cc-bank-info:get"
SCOPE_FACILITY_CC_DEPOSIT_IBAN_GET = "facility:cc-deposit-iban:get"
SCOPE_FACILITY_CARD_TO_DEPOSIT_GET = "facility:card-to-deposit:get"
SCOPE_BOOMRANG_WAGES_GET = "boomrang:wages:get"
SCOPE_BOOMRANG_TOKENS_GET = "boomrang:tokens:get"
SCOPE_BOOMRANG_TOKEN_DELETE = "boomrang:token:delete"
SCOPE_OAK_IBAN_INQUIRY_GET = "oak:iban-inquiry:get"
SCOPE_BOOMRANG_SMS_VERIFY_EXECUTE = "boomrang:sms-verify:execute"
SCOPE_BOOMRANG_SMS_SEND_EXECUTE = "boomrang:sms-send:execute"
SCOPE_FACILITY_DEPOSIT_IBAN = "facility:cc-deposit-iban:get"
SCOPE_KYC_IDENTIFICATION_INQUIRY = "kyc:identification-inquiry:get"

# Cache Keys
CACHE_TTL = 60 * 60 * 24 * 30  # 10 days
NATIONAL_CODE_MOBILE_VERIFICATION_CACHE_KEY = (
    ":finnotech:national-code-mobile-verification:%(national_code)s:%(mobile)s:"
)
POSTAL_CODE_INQUIRY_CACHE_KEY = ":finnotech:postal-code-inquiry:%(postal_code)s:"
CLIENT_IDENTIFICATION_INQUIRY_CACHE_KEY = (
    ":finnotech:client-identification-inquiry:%(national_code)s:%(birth_date)s:"
)
IBAN_INQUIRY_CACHE_KEY = ":finnotech:iban-inquiry:%(iban)s:"
DEPOSIT_TO_IBAN_CACHE_KEY = ":finnotech:deposit-to-iban:%(deposit)s:%(bank_code)s:"
BACK_CHEQUES_INQUIRY_CACHE_KEY = ":finnotech:back-cheques-inquiry:%(national_code)s:"

ALL_SCOPE_CLIENT_CREDENTIALS = [
    # SCOPE_OAK_IBAN_INQUIRY_GET,
    # SCOPE_CARD_INFORMATION_GET,
    # SCOPE_CARD_LIST_GET,
    # SCOPE_FACILITY_CARD_TO_IBAN_GET,
    # SCOPE_FACILITY_DEPOSIT_OWNER_VERIFICATION_GET,
    # SCOPE_FACILITY_CC_BANK_INFO_GET,
    # SCOPE_FACILITY_CC_DEPOSIT_IBAN_GET,
    # SCOPE_FACILITY_CARD_TO_DEPOSIT_GET,
    SCOPE_BOOMRANG_WAGES_GET,
    SCOPE_BOOMRANG_TOKENS_GET,
    SCOPE_BOOMRANG_TOKEN_DELETE,
    SCOPE_BOOMRANG_SMS_VERIFY_EXECUTE,
    SCOPE_BOOMRANG_SMS_SEND_EXECUTE,
]
ALL_SCOPE_AUTHORIZATION_TOKEN = [
    SCOPE_FACILITY_SMS_NID_VERIFICATION_GET,
    SCOPE_OAK_WITHDRAWAL_FROM_EXECUTE,
    SCOPE_OAK_TRANSFER_TO_EXECUTE,
    SCOPE_OAK_INQUIRY_TRANSFER_GET,
    SCOPE_OAK_PAYAS_GET,
    SCOPE_OAK_STATEMENT_GET,
    SCOPE_OAK_BALANCE_GET,
    SCOPE_OAK_USER_GET,
    SCOPE_OAK_DEPOSITS_GET,
    SCOPE_OAK_UNBLOCK_TRANSFER_INQUIRY_GET,
    SCOPE_OAK_BLOCK_,
    SCOPE_OAK_CHEQUE_,
    SCOPE_OAK_CARD_CHARGE_EXECUTE,
    SCOPE_OAK_CARD_CHARGE_INQUIRY_GET,
    SCOPE_OAK_VALID_CARD_GET,
    SCOPE_OAK_BILL_ACCOUNT_EXECUTE,
    SCOPE_KILID_REQUESTS_GET,
    SCOPE_KILID_REQUEST_CREATE,
    SCOPE_KILID_REQUEST_GET,
    SCOPE_KILID_REQUEST_DELETE,
    SCOPE_KILID_REQUEST_UPDATE,
]
