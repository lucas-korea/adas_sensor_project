import io
with io.open("RecFile_1_20210702_104356_stream2PCAP_1_output (Frame 0021) - Cloud.pcd",'rb') as f:
    fileContent = f.read()
    print(fileContent)
    print(str(fileContent))
    print(len(str(fileContent).split('\\n')))
    print(str(fileContent).split('\\n')[15])
    print(str(fileContent).split('\\n')[16])