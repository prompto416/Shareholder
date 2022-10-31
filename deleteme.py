from deep_translator import GoogleTranslator


translated1 = GoogleTranslator(source='auto', target='en').translate("บริษัท  THAI NVDR COMPANY LIMITED")
translated2 = GoogleTranslator(source='auto', target='en').translate("นาย บวรนวเทพ เทวกุล")
translated3 = GoogleTranslator(source='auto', target='en').translate("บริษัท  ศูนย์รับฝากหลักทรัพย์ (ประเทศไทย) จำกัด")
print((translated1).upper())
print((translated2).upper())
print((translated3).upper())

print(GoogleTranslator(source='auto', target='en').translate("บริษัท  THAI NVDR COMPANY LIMITED") == "THAI NVDR COMPANY LIMITED")

# print(translated1 in [])

print(type("S") == str)


                
print(translated3.upper())
print(translated2.upper())

f = open("deleteme.txt","a")
f.write("yo")




