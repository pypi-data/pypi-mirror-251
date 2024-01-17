from data_howdah import DataHowdah

df = DataHowdah('sample.csv')
df.encrypt([0])
df.to_csv('encrypted_data.csv', index=False)

df = DataHowdah('encrypted_data.csv')
df.decrypt()
df.to_csv('decrypted_data.csv', index=False)

df = DataHowdah('sample.csv')
df.mask([0], scale = 0.5, plots = True)
df.to_csv('encrypted_data.csv', index=False)