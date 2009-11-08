import k8055

import web

board = k8055.Board(address=0)

urls = (
    '/digitalout', 'digitalout',
    '/digitalout/(.*)', 'digitalout',
    '/(.*)', 'base'
)
app = web.application(urls, globals())

class base:        
    def GET(self, name):
        return board.__str__()

class digitalout:
    def GET(self, id=None):
        i=web.input(output="html")
        if id:
            try:
                id_no = int(id)
                if id_no >= 0 or id_no <=8:
                    if i.output == "json":
                        web.header('Content-Type', 'application/json')
                        return "{'D0%s':'%s'}" % (id_no, board.digital_outputs[id_no])
                    else:
                        return """<html><body><ul>
                              <li>Digital Out on %s - state: %s 
                              <form action="/digitalout/%s" method="POST">
                              <select name="id">
                              <option value="0">Off</option>
                              <option value="1">On</option>
                              </select>
                              <input type="submit" value="Change setting"/>
                              </form></li></ul></body></html> """ % (id_no, board.digital_outputs[id_no], id_no)
                else:
                    raise Exception
            except:
                pass
        output = """<html><body><ul>"""
        for x in xrange(8):
            output += "<li>Digital Out on %s - state: %s " % (x,board.digital_outputs[x])
            output += """<form action="/digitalout/%s" method="POST">
                              <select name="id">
                              <option value="0">Off</option>
                              <option value="1">On</option>
                              </select>
                              <input type="submit" value="Change setting"/>
                              </form> </li>""" % (x)
        output += "</ul></body></html>"
        return output

    def POST(self, id=None):
        if not id:
            raise web.found('/digitalout')
        else:
            try:
                id_no = int(id)
                if id_no >= 0 or id_no <=8:
                    i = web.input(id="Fail")
                    if i.id == "1":
                        board.digital_outputs[id_no] = 1
                    elif i.id != "Fail":
                        board.digital_outputs[id_no] = 0
                    board.set_digital_outputs()
                    raise web.found('/digitalout/%s' % id_no)
                else:
                    raise Exception
            except:
                pass
            raise web.found('/digitalout')

if __name__ == "__main__":
    app.run()

