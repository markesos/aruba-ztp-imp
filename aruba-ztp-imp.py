#!/usr/bin/python3


import csv 
# Load pyschedule and create a scenario with ten steps planning horizon

myinputfile  = r'ztp-2019-07-11.csv'
myoutoutfile = r'output50.csv'

stackdict = {}
switchdict = {}

with open(myinputfile) as csv_file:
	csv_reader = csv.reader(csv_file, delimiter=';')
	line_count = 0
	for row in csv_reader:
		line_count += 1

		#cellno = 1
		#for cell in row:
		#	print(f'\t{cellno}: {cell}')
		#	cellno += 1
			
		if row[2]:
			#print(f'\t switch:{row[1]}, mac: {row[2]}, vlan: {row[4]}')
			line_count += 1
			
			#stackdict['switch']  = row[1]
			switch  = row[0]
			stack   = switch[:7]
			print('switch:', switch)
			member  = switch[7]
			
			#if member == '1':
			#	switchname = stack
			#else:
			#	switchname = stack + '-' + member
			
			switchname = stack + '-' + member
			#switchname = stack	
			switch = switchname
			
			oldmac  = row[1]
			sn		= row[2]
			## obsolete 190712 vlan    = row[4]
			
			#mac = oldmac[0:2] + ':' + oldmac[2:4] + ':' + oldmac[4:6] + ':' + oldmac[6:8] + ':' + oldmac[8:10] +':' + oldmac[10:] + '+' + oldmac
			mac = oldmac[0:2] + ':' + oldmac[2:4] + ':' + oldmac[4:6] + ':' + oldmac[6:8] + ':' + oldmac[8:10] +':' + oldmac[10:]
			
			devdict = {}
			#devdict['switch'] = switch
			devdict['stack']  = stack
			devdict['member'] = member
			devdict['mac']    = mac
			devdict['sn']	  = sn
			#devdict['vlan']   = vlan
			devdict['vlan']   = '2901'
			
			print(devdict)
			
			switchdict[switch] = devdict
			
			
			
			if stack not in stackdict.keys():
				stackdict[stack] = {}
				#(stackdict[stack])['member1_mac'] = '00:00:00:00:00:00'
				#(stackdict[stack])['member2_mac'] = '00:00:00:00:00:00'
				#(stackdict[stack])['member3_mac'] = '00:00:00:00:00:00'
				#(stackdict[stack])['member4_mac'] = '00:00:00:00:00:00'
			
			if member == '1':
				(stackdict[stack])['member1_mac'] = mac
				
			if member == '2':
				(stackdict[stack])['member2_mac'] = mac
				
			if member == '3':
				(stackdict[stack])['member3_mac'] = mac
				
			if member == '4':
				(stackdict[stack])['member4_mac'] = mac

					
			
	print(f'Processed {line_count} lines.')

print(switchdict)
print(stackdict)
    
with open(myoutoutfile, "w+", newline='') as cvsFile:
	writer = csv.writer(cvsFile, delimiter=',') # delimeter = ';' for template; delimeter = ';' for EXCEL import 
	
	myrow = ('Modify authorized device', 'Sync dynamic variables', 'Name', 'LAN MAC Address', 'Serial Number', 'uksh_mgmt_vlan_id', 'uksh_mgmt_vlan_name', 'uksh_mgmt_wlan_id', 'uksh_mgmt_wlan_name', 'primary_radius', 'secondary_radius', 'stack_number', 'member1_mac', 'member2_mac', 'member3_mac', 'member4_mac', 'Group Name', 'Folder Name')
	writer.writerow(myrow)
	
	for myswitch, myswitchval in switchdict.items():
		print(myswitchval)
		
		stackbuff = stackdict[myswitchval['stack']]
		print(myswitchval['stack'])
		
		stacknum = 0
		
		if 'member1_mac' in stackbuff.keys():
			memb1 = stackbuff['member1_mac']
			stacknum = 1
		else: 
			memb1 = '00:00:00:00:00:00'
			
		if 'member2_mac' in stackbuff.keys():
			memb2 = stackbuff['member2_mac']
			stacknum = 2
		else: 
			memb2 = '00:00:00:00:00:00'
			
		if 'member3_mac' in stackbuff.keys():
			memb3 = stackbuff['member3_mac']
			stacknum = 3
		else: 
			memb3 = '00:00:00:00:00:00'
			
		if 'member4_mac' in stackbuff.keys():
			memb4 = stackbuff['member4_mac']
			stacknum = 4
		else: 
			memb4 = '00:00:00:00:00:00'
		
		myrow = ('1', '0', myswitchval['stack'], myswitchval['mac'], myswitchval['sn'], myswitchval['vlan'], 'SWI-NMM', '2935', 'WLAN-NMM', '172.29.90.80', '172.29.90.81', stacknum, memb1, memb2, memb3, memb4, 'grpZTP-2_Stack', 'Top')
		#myrow = "dummy"
		print(myrow)
		writer.writerow(myrow)    
cvsFile.close()


