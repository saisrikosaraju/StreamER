#Register Algorithm
#Arguments:Callback Function
#         :list of events interested in
#

def RegisterAlgorithm(func):
    print('Registering callback', func)
#    global func_name = func;

def TriggerCallback():
    print('Calling Trigger Callbac')
    func();
    
    
