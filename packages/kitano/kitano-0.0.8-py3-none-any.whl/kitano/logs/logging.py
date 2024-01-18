# ReinanBr 04/10/22
# lib: kitano
# LICENSE: MIT

from datetime import datetime
import time
import sys




#get date

strft='[%d/%m/%Y %H:%M:%S]:'



#show date
def str_date(strftime:str=strft) -> None:
    # if strftime==True:
    #     strftime= '[%H:%M:%S %d/%m/%Y]:'
    # else:
    #     strftime=''
    global strft
    strft = strftime
    datePrint = datetime.now().strftime(strft)
    return datePrint

#lib for pritting
def puts(*txt,sep=' ',
         end:str='\n',
         file_log:str=None,
         mode_write:str='a'):
	"""one way for printing info

	Args:
		*txt (optional): 
		sep (str, optional): a separation for more from one text. Defaults to ' '.
	"""
	txt_list = [str(i) for i in txt]
	txt_list.append(end)
	text_show = (sep).join(txt_list)
	date_prt = str_date(strft)
	prt_txt = f'{date_prt} {text_show}'
	sys.stdout.write(prt_txt)
	if file_log:
		with open(file_log,mode_write) as file_log_write:
			file_log_write.write(prt_txt)





# ''' class Puts'''
# class Puts:
	
# 	def __init__(self):
# 	  self.allDate = False
# 	  self.showDate = True
# 	  self.strfDate = False
# 	  self.sep = ' '
# 	  #pass
# 	#lib for pritting
# 	def puts(self,*txt):
# 	  textShowing = txt
# 	  if len(txt) > 1:
# 	    textShowing = (self.sep).join([str(text) for text in txt])
# 	  if self.showDate:
# 	    if self.strfDate:
# 	      datePrt = getDate(self.strfDate)
# 	      prtTxt = f'{datePrt}: {textShowing}'
# 	    else:
# 	      datePrt = getDate('[%H:%m:%S %d/%m]')
# 	      prtTxt = f'{datePrt}: {textShowing}'
# 	  else:
# 	    prtTxt = f'{textShowing}'
# 	  print(prtTxt)
