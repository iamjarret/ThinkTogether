class Collection(dict):
    def __init__(self, *args):
        dict.__init__(self, {h.name: h for h in args})
        self.original = self.keys()
    
    def __getitem__(self, key):
        if '-' in key:
            source, name = key.split('-')
            return super(Collection, self).__getitem__(source).get(name, None)
        else:
            return super(Collection, self).get(key, None)
    
    def flatten(self):
        flatten_keys = [h for h in self.keys() if h not in self.original]
        flattened_dict = dict([(h, self[h]) for h in flatten_keys])
        #add origin files
        for infoSet in self.original:
            for key, value in self[infoSet].items():
                new_key = "%s-%s"%(infoSet, key)
                flattened_dict.update({new_key:value})
        return flattened_dict


class InformationSet(dict):
    def __init__(self,name, *args):
        self.name = name
        dict.__init__(self,*args)


class InferenceSet(Collection):
    def __init__(self, name, *args):
        Collection.__init__(self, *args)
        self.name = name
    
    def inferred(self, return_informationset = True, return_dict = False):
        inferred_keys = [h for h in self.keys() if h not in self.original]
        inferred_dict = dict([(h, self[h]) for h in inferred_keys])
        if return_informationset:
            return InformationSet(self.name, inferred_dict)
        elif return_dict:
            return inferred_dict
        else:
            return inferred_keys
    
    def process(self, func, input=''):
    	if self.__repr__()!='{}':
            if input:
        	   self.update(func(input))
            else:
                self.update(func(self))
