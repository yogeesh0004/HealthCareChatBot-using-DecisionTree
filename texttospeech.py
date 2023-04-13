import googletrans
print(googletrans.LANGUAGES)
from googletrans import Translator
tr=Translator()
tp=tr.translate('Bonsoir',src='fr',dest='en')
print(tp.text)
