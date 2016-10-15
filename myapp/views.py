from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponseRedirect,HttpResponse
from .models import Node,TimeVolume
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
import json
from math import sqrt

def date_handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    else:
        raise TypeError

def serializable_object(nodee):
    color = "#fff"
    if not nodee.parent:
	obj = {'name': nodee.name,'age': nodee.age,'actual_state': nodee.actual_state,'time':10,'volume':10,'children': [],'colore':color,'ide':nodee.id,'clicked':False}
    else:
	tim = 200
	vol = 10
	tab = TimeVolume.objects.filter(node=nodee.id)
	if tab :
		last = tab.latest('datins')
		tim = last.time+150
		vol = sqrt(last.volume)+10
		color = "lightsteelblue"
		#print last.time
        obj = {'name': nodee.name,'parent': nodee.parent.name,'date': nodee.date,'tumor': nodee.tumor, 'anatomic_pathology': nodee.anatomic_pathology,'tumor_markers': nodee.tumor_markers,'site': nodee.site,'position': nodee.position,'treatment': nodee.treatment,'age': nodee.age,'actual_state': nodee.actual_state,'time':tim,'volume':vol,'children': [],'colore':color,'ide':nodee.id,'clicked':False}
    for child in nodee.get_children():
        obj['children'].append(serializable_object(child))
    return obj

@login_required
def show_trees(request):
    qs = Node.objects.root_nodes()
    return render(request,"show_trees.html",{'treeslist':qs})

@login_required
def show_node(request):
	if request.method == "POST":
		table=[]
		nod=request.POST.get("nod")
		print nod
		nodee = get_object_or_404(Node,id=nod)
		if nodee.is_root_node()== False:
			data ={'name':nodee.name,'root':False,'parent':nodee.parent.name,"pid":nodee.parent.id,'date':str(nodee.date),'tumor':nodee.tumor, 'anatomic_pathology':nodee.anatomic_pathology,'tumor_markers':nodee.tumor_markers,'site':nodee.site,'position':nodee.position,'treatment':nodee.treatment,'id':nodee.id,'leaf':nodee.is_leaf_node()}
			t = TimeVolume.objects.filter(node=nodee)
		        riga = list(t)
		        for i in range(len(t)):
				tdata={'time':t[i].time,'volume':t[i].volume,'node':t[i].node.id,'id':t[i].id}
				table.append(tdata)
		else:
			data = {'name':nodee.name,'root':True,'age': nodee.age,'actual_state': nodee.actual_state,'id':nodee.id,'leaf':nodee.is_leaf_node()}
		return HttpResponse(json.dumps({"datajs":data,"table":table}),content_type="application/json")

@login_required
def save_node(request):
	if request.method == "POST":
		nodee = get_object_or_404(Node,name=request.POST.get("name"))
		#if request.POST.get("isroot") == "si":
		if nodee.is_root_node():
			campi = {"name":request.POST.get("name"),"age":request.POST.get("age"),"actual_state":request.POST.get("actual_state")}
			formr = RootForm(campi or None,instance=nodee)
			#print "fooorm:"+str(formr)
			if formr.is_valid():
				print "saved r"
				instance = formr.save(commit=False)   
				instance.save()
		else:
			campi = {"name":request.POST.get("name"),"parent":request.POST.get("pid"),"date":request.POST.get("date"),"tumor":request.POST.get("tumor"),"anatomic_pathology":request.POST.get("anatomic_pathology"),"tumor_markers":request.POST.get("tumor_markers"),"site":request.POST.get("site"),"position":request.POST.get("position"),"treatment":request.POST.get("treatment")}
			formn = NodeForm(campi or None,instance=nodee)
                        #print "fooorm:"+str(formn)
			if formn.is_valid():
				print "saved n"
	            		instance = formn.save(commit=False)   
	            		instance.save()
		opt=request.POST.get("opt")
		root = get_object_or_404(Node,id=opt)
		jstree = json.dumps(serializable_object(root), default=date_handler)
		return HttpResponse(json.dumps({"datajs":jstree}),content_type="application/json")

@login_required
def delete_node(request):
	if request.method == "POST":
		nodee = get_object_or_404(Node,id=request.POST.get("hiddel"))
		opt=request.POST.get("opt")
		print nodee.id
		print opt
		if str(opt)==str(nodee.id):
			print "rrr"
			nodee.delete()
			jstree = "radice"
		else:
			print "nnn"
			nodee.delete()
			root = get_object_or_404(Node,id=opt)
			jstree = json.dumps(serializable_object(root), default=date_handler)
		return HttpResponse(json.dumps({"datajs":jstree}),content_type="application/json")

@login_required
def save_table(request):
	if request.method == "POST":
		ltim = request.POST.getlist("time")
		lvol = request.POST.getlist("volume")
		lid = request.POST.getlist("id")
		ldel = request.POST.getlist("delete")
		delete = None
		for i in range(len(ltim)):#save
			print "save"
			row = get_object_or_404(TimeVolume,id=lid[i])
			if int(ltim[i]) != int(row.time) or int(lvol[i]) != int(row.volume):
				campi = {"time":ltim[i],"volume":lvol[i],"node":request.POST.get("node")}
				print ltim[i] != row.time or lvol[i] != row.volume
				print campi
				formt = TableForm(campi or None,instance=row)
				if formt.is_valid():
				    	instance = formt.save(commit=False)   
				    	instance.save()
		if ldel : #delete
			print "delete"
			for i in range(len(ldel)):
				print ldel[i]
				row = get_object_or_404(TimeVolume,id=ldel[i])
				row.delete()
			delete = list(ldel)

		opt=request.POST.get("opt")
		root = get_object_or_404(Node,id=opt)
		jstree = json.dumps(serializable_object(root), default=date_handler)
		return HttpResponse(json.dumps({"datajs":jstree,"dele":delete}),content_type="application/json")

@login_required
def tree_details(request,name=None):
    if request.method == "POST":
	opt=request.POST.get("opt")
	root = get_object_or_404(Node,name=opt)#strdfvbjknlvcchgvjnklm DA CAMBIARE
	tree = root.get_family()
	disc = root.get_descendants()
	jstree = json.dumps(serializable_object(root), default=date_handler)
	node = None
        table = None
        form = None
        rdata = {'name':root.name,'age':root.age,'actual_state':root.actual_state}
	rform = RootForm(initial=rdata)

	if request.POST['submit'] == 'Go to tree':
	    return render(request,"tree_details.html",{'nodes':tree,'root':root,'disc':disc,'table':table,'form':form,'rform':rform,'jsonlist':jstree})	

@login_required
def create_root(request):
    form = RootForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)   
        instance.save()
    context = {"form":form}
    return render(request,"create_root.html",context)

@login_required
def create_node(request):
	if request.method == "POST":
		campi = {"name":request.POST.get("name"),"parent":request.POST.get("pid"),"date":request.POST.get("date"),"tumor":request.POST.get("tumor"),"anatomic_pathology":request.POST.get("anatomic_pathology"),"tumor_markers":request.POST.get("tumor_markers"),"site":request.POST.get("site"),"position":request.POST.get("position"),"treatment":request.POST.get("treatment")}
		form = NodeForm(campi or None)
		if form.is_valid():
			print "saved node"
            		instance = form.save(commit=False)   
            		instance.save()
			campi = {"time":request.POST.get("timee"),"volume":request.POST.get("volumee"),"node":instance.id}
			form = TableForm(campi or None)
		        #print "fooorm:"+str(formn)
			if form.is_valid():
				print "saved row"
		    		instance = form.save(commit=False)   
		    		instance.save()
    		opt=request.POST.get("opt")
		root = get_object_or_404(Node,id=opt)
		jstree = json.dumps(serializable_object(root), default=date_handler)
		print "sdahs"
		return HttpResponse(json.dumps({"datajs":jstree}),content_type="application/json")

@login_required
def insrow(request):
	if request.method == "POST":
		campi = {"time":request.POST.get("timee"),"volume":request.POST.get("volumee"),"node":request.POST.get("nid")}
		form = TableForm(campi or None)
                #print "fooorm:"+str(formn)
		if form.is_valid():
			#print "ttt"
            		instance = form.save(commit=False)   
            		instance.save()

		table=[]
		nod=request.POST.get("nid")
		nodee = get_object_or_404(Node,id=nod)
		if nodee.is_root_node()== False:
			#data ={'name':nodee.name,'root':False,'parent':nodee.parent.name,"pid":nodee.parent.id,'date':str(nodee.date),'tumor':nodee.tumor, 'anatomic_pathology':nodee.anatomic_pathology,'tumor_markers':nodee.tumor_markers,'site':nodee.site,'position':nodee.position,'treatment':nodee.treatment,'id':nodee.id}
			t = TimeVolume.objects.filter(node=nodee)
		        riga = list(t)
		        for i in range(len(t)):
				tdata={'time':t[i].time,'volume':t[i].volume,'node':t[i].node.id,'id':t[i].id}
				table.append(tdata)
		opt=request.POST.get("opt")
		root = get_object_or_404(Node,id=opt)
		jstree = json.dumps(serializable_object(root), default=date_handler)
		return HttpResponse(json.dumps({"datajs":jstree,"table":table}),content_type="application/json")

def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/myapp')




