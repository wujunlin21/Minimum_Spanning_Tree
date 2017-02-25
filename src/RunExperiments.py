#/python



import networkx as nx
import time
import sys



class RunExperiment:

	def parseEdges(self,graph_file):	
		multi_G=nx.MultiGraph()
		
		with open(graph_file, 'r') as graphs:
			first_line = graphs.readline()
			first_line=list(map(lambda x: int(x), first_line.split()))
			assert(len(first_line) == 2)
			num_node = first_line[0]
			num_edge = first_line[1]
			


			for line in graphs:
				#parse edge and weight
				edge_data = list(map(lambda x: int(x), line.split()))
				assert(len(edge_data) == 3)
				u,v,edge_weight = edge_data[0], edge_data[1], edge_data[2]
				multi_G.add_edge(u,v,weight=edge_weight)
			
		
		myG=nx.Graph()
		for u,v,data in multi_G.edges_iter(data=True):
			if myG.has_edge(u,v):
				if myG[u][v]["weight"]>data["weight"]:
					myG[u][v]["weight"]=data["weight"]
			else:
				myG.add_edge(u,v,weight=data["weight"])		
		
		return myG			



	def make_set(self,x):
		self.parent[x]=x	
		self.rank[x]=0

	def union(self,x1,x2):
		root_x1 = self.find(x1)
		root_x2=self.find(x2)
		if root_x1 == root_x2:
			return None
		if self.rank[root_x1]>self.rank[root_x2]:
			self.parent[root_x2]=root_x1
		else:
			self.parent[root_x1]=root_x2
			if self.rank[root_x1]==self.rank[root_x2]:
				self.rank[root_x2] = self.rank[root_x2]+1
		
	def find(self,x):
		if self.parent[x] != x:
			self.parent[x]=self.find(self.parent[x])
		return self.parent[x]


		
        def computeMST(self,G):
                self.parent=dict()
                self.rank=dict()	
                for node in G.nodes():
                                self.make_set(node)	
                sorted_edges=G.edges(data=True)
                sorted_edges.sort(key=lambda x:x[2]["weight"])
				
                self.MST=set()
                
                MST_w=0

                for edge in sorted_edges:
                        node1=edge[0]
                        node2=edge[1]
                        w=edge[2]["weight"]
                        if self.find(node1) != self.find(node2):
                                self.union(node1,node2)
                                self.MST.add((node1,node2,w))
                                MST_w=MST_w+w
                return MST_w
		

        def depth_first_search(self,route,start,end,path):
                path.append(end)
                if start==end:
                        return [end]
                if len(route[end])==0:
                        return None
                for item in route[end].items():
                        node=int(item[0])
                        weight=item[1]
                        if (node in path)==False:
                                findNext=self.depth_first_search(route,start,node,path)
                                if findNext is not None:
                                        temp_path=[end]+findNext
                                        return temp_path



                                

        def recomputeMST(self,u, v, weight_uv, G):
                nodes=G.nodes()
                route=[]
                for node in nodes:
                        route.append(dict())
                for edge in self.MST:
                        node1=edge[0]
                        node2=edge[1]
                        weight=edge[2]
                        route[node1][str(node2)]=weight
                        route[node2][str(node1)]=weight

                out_path=self.depth_first_search(route,u,v,path=[])

                max_weight=0
                for index in range(1,len(out_path)):
                        left=out_path[index-1]
                        right=out_path[index]
                        tempt_w=route[left][str(right)]
                        if tempt_w>max_weight:
                                max_weight=tempt_w
                                max_node1=left
                                max_node2=right

                if max_weight>weight_uv:
                        if (max_node1,max_node2,max_weight) in self.MST:
                                self.MST.remove((max_node1,max_node2,max_weight))
                        elif (max_node2,max_node1,max_weight) in self.MST:
                                self.MST.remove((max_node2,max_node1,max_weight))
                        self.MST.add((u,v,weight_uv))

                MST_w_recompute=sum(k for i,j,k in self.MST)
                return MST_w_recompute
                        

                        
                        
                        

	

	
        def main(self):

		num_args = len(sys.argv)

		if num_args < 4:
			print "error: not enough input arguments"
			exit(1)

		graph_file = sys.argv[1]
		change_file = sys.argv[2]
		output_file = sys.argv[3]


		#Construct graph
		G = self.parseEdges(graph_file) #TODO: read the graph file input

		
		start_MST = time.clock() #time in seconds
		MSTweight = self.computeMST(G) #TODO: return total weight of MST
		total_time = (time.clock() - start_MST) * 1000 #to convert to milliseconds

		#Write initial MST weight and time to file
		output = open(output_file, 'w')
		output.write(str(MSTweight) + " " + str(total_time) + "\n")

		#Changes file
		with open(change_file, 'r') as changes:
			num_changes = changes.readline()

			for line in changes:
				#parse edge and weight
				edge_data = list(map(lambda x: int(x), line.split()))
				assert(len(edge_data) == 3)

				u,v,weight = edge_data[0], edge_data[1], edge_data[2]

				#call recomputeMST function
				start_recompute = time.clock()
				new_weight = self.recomputeMST(u, v, weight, G) #TODO: return the weight of the modified MST
				total_recompute = (time.clock() - start_recompute) * 1000 # to convert to milliseconds

				#write new weight and time to output file
				output.write(str(new_weight) + " " + str(total_recompute) + "\n")

if __name__ == '__main__':
    # run the experiments
    myExperiment=RunExperiment()
    myExperiment.main()
