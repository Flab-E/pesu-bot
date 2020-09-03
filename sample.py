
file1 = open("batch_list.csv", "w")

stream = ['ME(EC)', 'S&H-PESU(EC)', 'BArch(RR)', 'BBA(RR)', 'BCA(EC)', 'S&H(RR)', 'CSE(EC)', 'EEE(RR)', 'CSE(RR)', 'CV(RR)', 'CIE', 'BDes(RR)', 'MCA(RR)', 'BBA-LLB(RR)', 'ECE(RR)', 'LLB', 'ME(RR)', 'ECE(EC)', 'BBA(EC)', 'BBA-HEM(RR)', 'BT(RR)', 'MBA(RR)']
hostel = ["NA", "A"]

for i in range(2):
    for j in range(len(stream)):
        for k in range(3):
            SRN = "PES"+str(i+1)+"UG19"+stream[j].split("(")[0].replace("BBA-HEM", "BH")+ (str(k+1).zfill(3))
            PRN = "PES" + str(i+1) + "20190" + (str(k+1).zfill(4))
            sem = "Sem-3"
            Section = "Section " + str(ord("A") + k)
            host = hostel[k%2] 
            sc = stream[j].split("(")[0] +" (RR Campus)"
            st = stream[j]
            camp = "PES University (Ring Road)"
            line = ",".join([SRN, PRN, sem, Section, host, sc, st, camp])
            file1.write(line+"\n")
file1.close()
