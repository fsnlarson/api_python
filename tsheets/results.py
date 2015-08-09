import logger

class Results(object):
    def __init__(self, url, options, model, bridge, cache, is_singleton=False, mode="list"):
        self.url = url
        self.options = options
        self.model = model
        self.name = "users" #todo
        self.index = -1
        self.loaded = []
        self.bridge = bridge
        self.cache = cache
        self.has_more = True
        self.is_singleton = is_singleton
        self.mode = mode

    def __iter__(self):
        return self

    def next(self):
        if (self.index+1) < len(self.loaded) or (self.has_more and self.__load_next_batch()):
            self.index += 1
            next_value = self.loaded[self.index]
            print next_value
            return next_value
        else:
            raise StopIteration


    def all(self):
        return list(self)

    def __load_next_batch(self):
        response = self.bridge.next_batch(self.url, self.name, self.options, self.is_singleton, self.mode)
        batch = response['items']
        print "Batch"
        print batch
        self.has_more = not self.is_singleton and self.mode == 'list' and response['has_more']
        if self.is_singleton:
          self.loaded = [ self.model.from_raw(batch) ]
        else:
          self.loaded += [self.model.from_raw(o) for o in batch ]
        return batch
