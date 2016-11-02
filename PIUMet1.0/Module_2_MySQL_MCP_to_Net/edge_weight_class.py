#this class is describing a weight asscoiated to an edge and have function to normalize it
#
#
#by: Leila Pirhaji
#----------------------------------


class edge_weight_class(object):
	def __init__(self, net, edge):		
		source_weight_dic=net[edge[0]][edge[1]]['source_weight']
		self.normalized_w_list=[]
		for source in source_weight_dic.keys():
			if source[:9]=='iRefIndex':
				if float(source_weight_dic[source]) > 1:
					self.normalized_w_list.append(1)
				elif float(source_weight_dic[source]) < 0:
					self.normalized_w_list.append(0)
				else:
					self.normalized_w_list.append(float(source_weight_dic[source]))
			elif source=='Recon_2':
				self.Normalizing_Recon_edge_weights(float(source_weight_dic[source]))
			elif source[:5]=='STICH':
				self.Normalizing_STICH_edge_weights(float(source_weight_dic[source]))
			elif source=='PharmGKB_OffSide':
				self.Normalizing_PharmGKB_OffSide_edge_weights()
			elif source=='PharmGKB_Relationship':
				self.Normalizing_PharmGKB_Relationship_edge_weights(source_weight_dic[source])
			elif source=='SIDER':
				self.Normalizing_SIDER_edge_weights()
		#-----------------------
		#I consider the weight of an edge the maximum weight from a source
		self.weight=max(self.normalized_w_list)
	#--------------------------------
	#Normalizing Recon_2 edge weights
	def Normalizing_Recon_edge_weights(self,source_weight):
		if source_weight==0:
			self.normalized_w_list.append(0.4)
		elif source_weight==1:
			self.normalized_w_list.append(0.34)
		elif source_weight==2:
			self.normalized_w_list.append(0.4)
		elif source_weight==3:
			self.normalized_w_list.append(0.45)
		elif source_weight==4:
			self.normalized_w_list.append(1.00)	
	#--------------------------------
	#Normalizing STICH edge weights
	def Normalizing_STICH_edge_weights(self, source_weight):
		w=source_weight/1000
		self.normalized_w_list.append(w)
	#--------------------------------
	#Normalizing PharmGKB_OffSide edge weights
	def Normalizing_PharmGKB_OffSide_edge_weights(self):
		pass
	#--------------------------------
	#Normalizing PharmGKB_Relationship edge weights
	def Normalizing_PharmGKB_Relationship_edge_weights(self,source_weight):
		if source_weight=='associated':
			self.normalized_w_list.append(1.00)
		elif source_weight=='ambiguous':
			self.normalized_w_list.append(0.4)
		elif source_weight==' not associated':
			self.normalized_w_list.append(0.00)
	#--------------------------------
	#Normalizing SIDER edge weights
	def Normalizing_SIDER_edge_weights(self,source_weight):
		if source_weight=='frequent':
			self.normalized_w_list.append(1.00)
		elif source_weight=='infrequent':
			self.normalized_w_list.append(0.4)
		elif source_weight=='postmarketing':
			self.normalized_w_list.append(0.4)
		elif source_weight=='potential':
			self.normalized_w_list.append(0.45)
		elif source_weight=='rare':
			self.normalized_w_list.append(0.34)
		elif source_weight[-1:]=="%":
			source_weight=source_weight.replace(" ","").strip("%s")
			if source_weight.find('-')==-1 and source_weight.find('to')==-1:
				source_weight=float(source_weight)/100
				self.normalized_w_list.append(source_weight)
			elif  source_weight.find('-')==-1:
				source_weight=source_weight.split('to')
				w_range=[float(w) for w in source_weight]
				self.normalized_w_list.append(sum(w_range)/len(w_range))
			else:
				source_weight=source_weight.split('-')
				w_range=[float(w) for w in source_weight]
				self.normalized_w_list.append(sum(w_range)/len(w_range))		
			