from django.shortcuts import render
from django.http import JsonResponse
import requests
import time
import pandas as pd
import re
import cv2
import pdb
import glob
import datefinder
import numpy as np
from django.http import HttpResponse
from rest_framework.response import Response
import base64
from datetime import datetime as dt
import os
import dateutil.parser as dparser
from .models import models
from .forms import imageForm


def home(request):
	# base64_string=" "
	if request.method=="POST":
		form=imageForm(request.POST or None)
		if form.is_valid():
			# base64_string=form.save(commit=False)
			# base64_string.save()
			data=form.cleaned_data
			res=data['image_string']
			# print(res)
			# date_extract(request,res)
			# date_extract(request,res)	
			return (res)
			# HttpResponseRedirect('/date')

	else:
	  form=imageForm()
	return render(request,'base644.html',{'form':form})
	# return date_extract(request,res,form)	
	# pdb.set_trace()


def date_extract(request):
	res=home(request)
	print(res)


	
	_url = 'https://southeastasia.api.cognitive.microsoft.com//vision/v2.0/recognizeText'
	_key = "c18117db615f4e1f98116e8c7de42617"
	_maxNumRetries = 10

	def result_microsoft_api(filepath):
		
		pathToFileInDisk = filepath
		with open(pathToFileInDisk, 'rb') as f:
			data = f.read()

		params = {'mode' : 'Printed'}
		headers = dict()
		headers['Ocp-Apim-Subscription-Key'] = _key
		headers['Content-Type'] = 'application/octet-stream'
		headers["Access-Control-Allow-Origin"]=  "*"

		json = None
		operationLocation = processRequest(json, data, headers, params)
		result = None
		if (operationLocation != None):
			headers = {}
			headers['Ocp-Apim-Subscription-Key'] = _key
			headers["Access-Control-Allow-Origin"]=  "*"
			while True:
				time.sleep(1)
				result = getOCRTextResult(operationLocation, headers)
				if result['status'] == 'Succeeded' or result['status'] == 'Failed':
					break
		try:
			lines = result['recognitionResult']['lines']
			return lines
		except:
			return None


	def getOCRTextResult( operationLocation, headers ):

		retries = 0
		result = None

		while True:
			response = requests.request('get', operationLocation, json=None, data=None, headers=headers, params=None)
			if response.status_code == 429:
				print(("Message: %s" % (response.json())))
				if retries <= _maxNumRetries:
					time.sleep(1)
					retries += 1
					continue
				else:
					print('Error: failed after retrying!')
					break
			elif response.status_code == 200:
				result = response.json()
			else:
				print(("Error code: %d" % (response.status_code)))
				print(("Message: %s" % (response.json())))
			break

		return result


	def processRequest( json, data, headers, params ):
		retries = 0
		result = None

		while True:
			response = requests.request( 'post', _url, json = json, data = data, headers = headers, params = params )
			time.sleep(5)
			print((response.status_code))
			if response.status_code == 429:
				print(( "Message: %s" % ( response.json() ) ))
				if retries <= _maxNumRetries: 
					time.sleep(1) 
					retries += 1
					continue
				else: 
					print( 'Error: failed after retrying!' )
					break
			elif response.status_code == 202:
				result = response.headers['Operation-Location']
			else:
				print(( "Error code: %d" % ( response.status_code ) ))
				print(( "Message: %s" % ( response.json() ) ))
			break
			
		return result


	def get_text_bounding_boxes(micro_soft_ocr):
		text_bounding_box_info = []
		for text_info in micro_soft_ocr:
			bounding_box_info = {}
			bounding_box_info['boundingBox'] = text_info['boundingBox']
			bounding_box_info['text'] = text_info['text']
			text_bounding_box_info.append(bounding_box_info)
		return text_bounding_box_info

	def get_OCR_results(image_path):

		micro_soft_ocr = result_microsoft_api(image_path)
		text_bounding_boxes = get_text_bounding_boxes(micro_soft_ocr)

		return text_bounding_boxes

	

	counter = 0
	recipt_list = []

	
	imgdata = base64.b64decode(res)
	filename = 'some_image1.jpeg' 
	with open(filename, 'wb') as f:
		f.write(imgdata)
	
	result = get_OCR_results('some_image1.jpeg')
	
	for box in result :
		recipt_list.append([box['text']])

	df = pd.DataFrame(recipt_list, columns=['text'])

	df['dates'] = df['text'].str.extract(r'([\d]{1,2}/[\d]{1,2}/[\d]{2,4}|[\d]{1,2}-[\d]{1,2}-[\d]{2,4}|[\d]{1,2}-[ADFJMNOS]\w*-[\d]{2,4}|[\d]{1,2}-[ADFJMNOS]\w* - [\d]{2,4}|[ADFJMNOS]\w* [\d]{1,2}\. [\d]{2,4})', expand = True)

	df['is_date'] = df.dates[df.dates.notnull()]

	df.is_date[df.is_date.notnull()] = True
	df.is_date[df.is_date == True]

	df = df.dropna()

	df.reset_index()


	date = []
	for i in df.text.to_list():
		try:
			date.append(dparser.parse(i,fuzzy=True))
		except:
			date.append('no date')


	df['date_avail'] = date

	df.loc[df.date_avail == 'no date']



	df.loc[df.date_avail != 'no date','dates'] = df[df.date_avail != 'no date'].date_avail

	df.loc[df.date_avail != 'no date','date_avail'] = [x.split(' ')[0] for x in df.date_avail.astype('str').to_list() if 'no date' not in x]

	date_output = df['date_avail'].to_string(index=False)
	print(date_output)
	

	if df.date_avail.dtype != 'float64':
		# return HttpResponse(request,{'date':date_output})
		return render(request,'output.html',{'date_output':date_output})
		# return JsonResponse({'date_output':date_output}, status=201)
		
	else:
		# return HttpResponse(request,{'date':"null"})
		return render(request,'output.html',{'date_output':"null"})
		# return JsonResponse({'date_output':"null"}, status=201)



# def redirect_course(request):
#         date_extract(request)
#         return redirect('results/')
# ~                                        





