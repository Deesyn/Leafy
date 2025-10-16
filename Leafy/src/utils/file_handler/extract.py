class extract:
    @staticmethod
    def zip(path):
        import zipfile
        with zipfile.ZipFile(path, 'r') as f:
            return f
    @staticmethod
    def rar(path):
        import rarfile
        with rarfile.RarFile(path,'r') as f:
            return f