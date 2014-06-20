# encoding=utf-8
# author : lifuxin1125@gmail.com
# date: 2014-06-20
# version: 0.1

'''
    将各个属性进行整理，然后得到特征矩阵:
    得到的特征矩阵分为三类：
        1.
'''
if __name__ == "__main__":
    # 输入：
    precontentfilename = "../Output/precontent"
    sentimentfilename = "../Output/sentiment"
    yearfilename = "../Output/year"
    monthfilename = "../Output/month"
    dayfilename = "../Output/day"
    hourfilename = "../Output/hour"
    minfilename = "../Output/min"
    publicwordPMIfilename = "../Dictionary/publicwordPMI"
    nonpublicwordpmifilename = "../Feature/nonpublicwordfreqge2"

    # 输出：
    FMatrixWithNPWfilename = "../Feature/FeatureMatrixWithNPW"
    FMatrixWithNPWsetZerofilename = "../Feature/FeatureMatrixWithNPWsetZero"
    FMatrixWithoutNPWfilename = "../Feature/FeatureMatrixWithoutNPW"

    arffwithNPWriter = open(FMatrixWithNPWfilename,"w")
    arffwithNPsetzeroWriter = open(FMatrixWithNPWsetZerofilename,"w")
    arffwithoutNPWriter = open(FMatrixWithoutNPWfilename,"w")

    emocNo=6962
    negNo = 6963
    yearNo = 6964
    monthNo = 6965
    dayNo = 6966
    hourNo = 6967
    minNo = 6968
    sentimentNo = 6969
    try:
        sentimentreader = open(sentimentfilename,"r")
        yearreader = open(yearfilename,"r")
        monthreader = open(monthfilename,"r")
        dayreader = open(dayfilename,"r")
        hourreader = open(hourfilename,"r")
        minreader = open(minfilename,"r")
        publicwordreader = open(publicwordPMIfilename,"r")
        nonpublicwordreader = open(nonpublicwordpmifilename,"r")
    except:
        print "error IO"

    tweetNo=1
    tweetdic={}
    for sentiment in sentimentreader:
        tweetlis=[]
        tweetlis.append(sentiment.strip())
        year = yearreader.readline().strip()
        month = monthreader.readline().strip()
        day = dayreader.readline().strip()
        hour = hourreader.readline().strip()
        min = minreader.readline().strip()
        tweetlis.extend([year,month,day,hour,min])
        tweetdic[tweetNo]=tweetlis
        tweetNo = tweetNo +1
    sentimentreader.close()
    yearreader.close(),monthreader.close(),dayreader.close(),hourreader.close(),minreader.close()

    wordNO=1
    publicworddic = {}
    for publicword in publicwordreader:
        wordvalue = publicword.strip().split()
        publicworddic[wordvalue[0]] = [wordvalue[1],wordNO]
        wordNO = wordNO+1
    publicwordreader.close()

    nonpublicworddic = {}
    for nonpublicword in nonpublicwordreader:
        wordvalue=nonpublicword.strip().split()
        nonpublicworddic[wordvalue[0]] = [wordvalue[1],wordNO]
        wordNO = wordNO+1
    nonpublicwordreader.close()

    num_publicword = publicworddic.__len__()
    num_nonpublicword = nonpublicworddic.__len__()
    numtextfeature = publicworddic.__len__()+nonpublicworddic.__len__()



    tweetNo = 0
    with open(precontentfilename,"r") as contentreader:
        for tweetcontent in contentreader:
            tweetNo = tweetNo+1
            arffwithNPWriter.write("{"), arffwithoutNPWriter.write("{"),arffwithNPsetzeroWriter.write("{")
            wordarr = tweetcontent.strip().split()
            num_EMO=0
            num_NEG=0
            num_ADD_MIN=0
            wordarrdic={}
            wordwithNPsetzerodic={}
            wordwithoutNPdic={}
            for word in wordarr:
                # 公共情感词
                if word in publicworddic.keys():
                    wordarrdic[publicworddic[word][1]]=publicworddic[word][0]
                    wordwithNPsetzerodic[publicworddic[word][1]]=publicworddic[word][0]
                    wordwithoutNPdic[publicworddic[word][1]]=publicworddic[word][0]
                    #arffwithNPWriter.write(str(publicworddic[word][1])+" "+str(publicworddic[word][0])+",")
                elif word in nonpublicworddic.keys():
                    wordarrdic[nonpublicworddic[word][1]]=nonpublicworddic[word][0]
                    wordwithNPsetzerodic[nonpublicworddic[word][1]]=0
                    #arffwithNPWriter.write(str(nonpublicworddic[word][1])+" "+str(nonpublicworddic[word][0])+",")
                elif word == "POSEMOC":
                    num_EMO = num_EMO+1;
                elif word == "NEGEMOC":
                    num_EMO = num_EMO - 1;
                elif word == "NEGWORD":
                    num_NEG = num_NEG+1
                elif word == "POSADD":
                    num_ADD_MIN = num_ADD_MIN +1
                elif word == "NEGMIS":
                    num_ADD_MIN = num_ADD_MIN -1
            wordarrdiclist = sorted(wordarrdic.items())
            for wordNo,value in wordarrdiclist:
                arffwithNPWriter.write(str(wordNo)+" "+str(value)+",")

            wordwithoutNPWdiclist = sorted(wordwithoutNPdic.items())
            for wordNo,value in wordwithoutNPWdiclist:
                arffwithoutNPWriter.write(str(wordNo)+" "+str(value)+",")

            wordwithNPsetzerodiclist = sorted(wordwithNPsetzerodic.items())
            for wordNo,value in wordwithNPsetzerodiclist:
                arffwithNPsetzeroWriter.write(str(wordNo)+" "+str(value)+",")

            arffwithNPWriter.write(str(emocNo)+" "+str(num_EMO)+","+str(negNo)+" "+str(num_NEG)+","+
                str(yearNo)+" "+str(tweetdic[tweetNo][1])+","+
                str(monthNo)+" "+str(tweetdic[tweetNo][2])+","+
                str(dayNo)+" "+str(tweetdic[tweetNo][3])+","+
                str(hourNo)+" "+str(tweetdic[tweetNo][4])+","+
                str(minNo)+" "+str(tweetdic[tweetNo][5])+","+
    #            str(addminNo)+" "+str(num_ADD_MIN)+","+
                str(sentimentNo)+" "+tweetdic[tweetNo][0]+"}\n")

            arffwithoutNPWriter.write(str(emocNo)+" "+str(num_EMO)+","+str(negNo)+" "+str(num_NEG)+","+
                                   str(yearNo)+" "+str(tweetdic[tweetNo][1])+","+
                                   str(monthNo)+" "+str(tweetdic[tweetNo][2])+","+
                                   str(dayNo)+" "+str(tweetdic[tweetNo][3])+","+
                                   str(hourNo)+" "+str(tweetdic[tweetNo][4])+","+
                                   str(minNo)+" "+str(tweetdic[tweetNo][5])+","+
    #                               str(addminNo)+" "+str(num_ADD_MIN)+","+
                                   str(sentimentNo)+" "+tweetdic[tweetNo][0]+"}\n")

            arffwithNPsetzeroWriter.write(str(emocNo)+" "+str(num_EMO)+","+str(negNo)+" "+str(num_NEG)+","+
                                      str(yearNo)+" "+str(tweetdic[tweetNo][1])+","+
                                      str(monthNo)+" "+str(tweetdic[tweetNo][2])+","+
                                      str(dayNo)+" "+str(tweetdic[tweetNo][3])+","+
                                      str(hourNo)+" "+str(tweetdic[tweetNo][4])+","+
                                      str(minNo)+" "+str(tweetdic[tweetNo][5])+","+
    #                                  str(addminNo)+" "+str(num_ADD_MIN)+","+
                                      str(sentimentNo)+" "+tweetdic[tweetNo][0]+"}\n")
    contentreader.close()


    arffwithNPWriter.flush(),arffwithNPWriter.close()
    arffwithoutNPWriter.flush(),arffwithoutNPWriter.close()
    arffwithNPsetzeroWriter.flush(),arffwithNPsetzeroWriter.close()


