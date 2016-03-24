from view.baseview import *


class CViewMgr(BaseView):
    
    def info_view(self,params):
        out = []
        out.append(params)
        tbl_th = []
        tbl_key = []
        for k in params:
            tbl_th.append(k.upper())
            tbl_key.append(k)
        return self.common_list(tbl_th, tbl_key, data=out)

    def list_view(self,params,sort = False,count = True,key_list = None):
        if len(params) == 0 :
            return str('nothing to list')
        if not key_list:
            params = self.set_key_value_format(params)
        out = []
        index = 0
        for i in params:
            temp = {}
            temp['index'] = index
            if i.has_key('id'):
                if not i.has_key('name'):
                    i['name'] = i['id']
                    i.pop('id')
            temp.update(i)
            index = index + 1
            out.append(temp)
        if not key_list:
            tbl_key = self.get_common(out)
        else:
            key_list.insert(0,'index')
            tbl_key = key_list

        tbl_th = []
        for k in tbl_key:
            tbl_th.append(k.upper())
        return self.common_list(tbl_th, tbl_key, data=out,sort = sort,count = count)


    def error_view(self,params):
        pass

    def get_common(self,params):
        my_params = list(params)
        common = my_params[0]
        common_back = dict(common)
        my_params.remove(common)
        for para in my_params:
            for key in common_back:
                if (key not in para.keys() and key in common.keys()):
                    common.pop(key)
        common_key_list = common.keys()
        common_key_list.remove('index')
        common_key_list.insert(0,'index')
        if 'group' in common_key_list:
            common_key_list.remove('group')
            common_key_list.insert(1,'group')
        if 'name' in common_key_list:
            common_key_list.remove('name')
            common_key_list.insert(1,'name')
        return common_key_list

    def set_key_value_format(self,params):
        new_params = []
        if len(params) != 1 or len(params[0]) < 8:
            return params
        for key in params[0]:
            tmp = {}
            tmp['key'] = key
            tmp['value'] = params[0].get(key)
            new_params.append(tmp)
        return new_params
