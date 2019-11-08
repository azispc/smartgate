import face_recognition as citra

#fungsi panggil fungsi
while True:
    hasil=input("masukkan jarak:")
    if(float(hasil)>10):
        print("\n Jarak Memenuhi Syarat")
        hasil=citra.fungsirecognetion()
        print(hasil)

    else:
        # Do a bit of cleanup
        print("\n Jarak Tidak Memenuhi Syarat")
