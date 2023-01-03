import requests
from bs4 import BeautifulSoup
import re
import numpy as np
import logging
from colorlog import ColoredFormatter
    
class Gmail() :
    # def __init__(self, email) :
    #     self.__email = email
    LOG_LEVEL = logging.DEBUG
    LOGFORMAT = "  %(log_color)s%(levelname)-8s%(reset)s | %(log_color)s%(message)s%(reset)s"
    
    logging.root.setLevel(LOG_LEVEL)
    formatter = ColoredFormatter(LOGFORMAT)
    stream = logging.StreamHandler()
    stream.setLevel(LOG_LEVEL)
    stream.setFormatter(formatter)
    log = logging.getLogger('pythonConfig')
    log.setLevel(LOG_LEVEL)
    log.addHandler(stream)

    
    UserAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"

    base_url = "https://accounts.google.com/signup/v2/webcreateaccount"
    
    check_url = "https://accounts.google.com/_/signup/webusernameavailability"
    
    # check_email = "allisonmil@gmail.com"
    email_list = ['one@gmail.com','two@gmail.com','rivee@gmail.com']
    proxies_gmail = {
        'http': 'http://ip:port',
        'https': 'http://ip:port',
        }
    #start session 
    session = requests.Session()
    
    headerss = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'X-Same-Domain': '1',
        'Google-Accounts-XSRF': '1',
        'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
        'Origin': 'https://accounts.google.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://accounts.google.com/signup/v2/webcreateaccount?hl=en&flowName=GlifWebSignIn&flowEntry=SignUp',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        
    }   
    
    Data = {
        'hl': 'en',
        'flowName': 'GlifWebSignIn',
        'flowEntry': 'SignUp',
    }
        
    
    response= session.get(url=base_url, params=Data, headers=headerss, proxies=proxies_gmail, allow_redirects=True, timeout=3)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content,"html.parser")
        #start getting the payload data (f.req)
        try:
            
            Freq_data = soup.find_all("div", {'id':'view_container'})
            Freq_setup = Freq_data[0]['data-initial-setup-data']            
            freq= re.findall(r"(AETh\w+.[A-z,0-9]+.\S+.[A-z,0-9]-[A-z,0-9]+)",Freq_setup)
            f_req_S = freq[0]
          
        except Exception as e:
            log.warning('facing erros with f.req data |',str(e))
        Freq2 = soup.find_all('script',{'data-id':"_gd"})
        try :
           
            if "Qzxixc" in str(Freq2) :
                dd = re.findall("(Qzxixc\":\")(\D-?[A-z,0-9]+:[A-z,0-9]+)",str(Freq2))
                ss = np.array(dd)
                fp2 = ss[:,1][0]
            else :
                log.warning('Missing data from Request! %s'%response.text)
        except Exception as e:
            print("Error in side two of Freq data |",str(e))
            
        #start getting azt data 
        try :
            if "xsrf" in str(Freq2) :
                azt = re.findall("AFoag[A-z,0-9]+-?-?\w+:[0-9]+",str(Freq2))
            else :
                log.warning('Missing data from Request! %s'%response.text)
        except Exception as e:
            log.warning("Error in azt payload data| ",str(e))
        
        #start sending request 
        log.warning('*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*- Start Checking Gmail  -*-*-*-*-*-*-*-*-*-*-*-*-*-*')
        for i in email_list :
            user =  i.split('@')[0]
            payload  ={
                    "flowEntry": "SignUp",
                    "flowName": "GlifWebSignIn",
                    "hl": "en",
                    "continue": "https://accounts.google.com/ManageAccount?nc=1",
                    "f.req": "[\"%s\",\"\",\"\",\"%s\",true,\"%s\",1]"%(f_req_S,user,fp2),
                    "azt": azt[0],
                    "cookiesDisabled": "false",
                    "deviceinfo": "[null,null,null,[],null,\"IT\",null,null,null,\"GlifWebSignIn\",null,[null,null,[],null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,[],null,null,null,null,[]],null,null,null,null,0,null,false,1,\"\"]",
                    "gmscoreversion": "undefined",
                    "": ""
                }
            # check_emails = session.post()
            check_num_list = [1,2,3]
            try :
                check_request = session.post(check_url,params=Data,proxies=proxies_gmail,headers=headerss,data=payload,allow_redirects=True)
                resp_check = [check_request.text.replace('\n','')]                
                msg= resp_check[0][20:].replace('"]]',"")
           
                if check_request.status_code == 200 :
                    try  :                   
                    #get number 
                        N_check = re.findall("(gf.wuar\",)([0-9])",str(resp_check))
                        s_ch = np.array(N_check)
                        N_y = s_ch[:,1][0]
                        Check_Num_req = int(N_y)
                        try : 
                            if Check_Num_req in check_num_list :
                                
                                if Check_Num_req == 1 :
                                    # print("Valid username : [%s]"%user)
                                    log.info("Valid UserName : [{}]".format(user))
                                    print('*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*')
                                elif Check_Num_req == 2:
                                    try :
                                        if len(msg) != 0 :
                                        # suggestion username
                                            suggestion_UserName = msg.replace("]","")
                                            # print("This username [%s] is taken. Try another. "%user)
                                            log.error("This username [{}] is taken. Try another. ".format(user))
                                            log.info("Available Suggestion UserName : {}".format(suggestion_UserName))
                                            # log.warning('*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*')
                                            print('*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*')
                                            # print("Available: [%s]"%suggestion_UserName)
                                        else :
                                            # print("This username [%s] is taken. Try another. "%user)
                                            log.error("This username [{}] is taken. Try another. ".format(user))
                                            print('*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*')
                                        
                                    except Exception as e:
                                        log.warning("error to find this emails list")
                                        
                                else :
                                    log.error('Error Invalid UserName [%s]. '%user)
                                    log.info(msg)
                        except Exception as e :
                            log.warning("Error to start checking ",str(e))

                    except Exception as e:
                        log.warning(str(e))
                else :
                    log.warning('Error In Post Requests! %s %s'%(user,check_request.text))
                                       
            except Exception as e:
                log.error('error in post request |',str(e))
                
        log.warning('*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*- Ending Checking Gmail  -*-*-*-*-*-*-*-*-*-*-*-*-*-*')    