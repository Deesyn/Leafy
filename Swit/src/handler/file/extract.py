class extract:
    @staticmethod
    def zip(path):
        import zipfile
        return zipfile.ZipFile(path, 'r')

    @staticmethod
    def rar(path):
        import rarfile
        return rarfile.RarFile(path, 'r')
