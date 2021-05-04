class Principal:
    """
    A security principal represented by a certificate subject and the secret key.
    Used to authenticate the caller, whether it is a client to server or server
    to server call.
    """

    def __init__(self, subject, secret_key):
        """
        Creates an immutable security principal object.

        :param subject: principal/certificate subject
        :type subject: str
        :param secret_key: str: secret/private key
        :type secret_key str
        """
        self._subject = subject
        self._secret_key = secret_key

    def subject(self):
        """
        :return: principal/certificate subject
        :rtype str
        """
        return self._subject

    def secret_key(self):
        """
        :return: str: secret/private key
        :rtype str
        """
        return self._secret_key
