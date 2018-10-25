class Record:
    def __init__(self, cryptography, is_genesis=False):
        self.is_genesis = is_genesis
        self.cryptography = cryptography

    # calculate signature
    def calculate_signature(self):
        signature = self.cryptography.sign(self.format_record())
        self.signature = signature

    # check signature
    def check_signature(self):
        return self.cryptography.verify(
            self.format_record(),
            self.signature,
            self.from_pubkey
        )
