import array
import urllib
from java.io import PrintWriter
from burp import IBurpExtender, IHttpListener



class BurpExtender(IBurpExtender, IHttpListener):
    special_parameter = "custom_headers"

    def registerExtenderCallbacks(self, callbacks):
        self.helpers = callbacks.getHelpers()
        self.stdout = PrintWriter(callbacks.getStdout(), True)
        self.stderr = PrintWriter(callbacks.getStderr(), True)

        self.stdout.println("Extension is Loaded")

        callbacks.setExtensionName("Jenkins CI")
        callbacks.registerHttpListener(self)
        return

    def getAbsPathAndRequestParameters(self, path):
        abs_path, parameter_string = path.split("?", 1)
        parameters = {}
        if parameter_string:
            parameter_list = parameter_string.split("&")

            for p in parameter_list:
                key, value = p.split("=", 1)
                parameters[key] = value
        
        return abs_path, parameters
    
    def processHttpMessage(self, tool_flag, message_is_request, message_info):
        if message_is_request:
            request = message_info.getRequest()
            request_info = self.helpers.analyzeRequest(request)

            headers = request_info.getHeaders()
            # self.stdout.println(str(request_info.getParameters()))

            method, path, version = headers[0].split(" ")
            if "?" in path:
                abs_path, parameters = self.getAbsPathAndRequestParameters(path)

                if parameters:
                    special_parameter = parameters.get(self.special_parameter, "")
                    if special_parameter:
                        special_parameter = self.helpers.bytesToString(self.helpers.urlDecode(self.helpers.stringToBytes(special_parameter)))
                        try:
                            custom_headers_bytes = self.helpers.base64Decode(special_parameter)
                            custom_headers_string = self.helpers.bytesToString(custom_headers_bytes)
                            for custom_header in custom_headers_string.split("&"):
                                key, value = custom_header.split("=", 1)
                                headers.append(key + ": " + value)
                            
                            parameters.pop(self.special_parameter)
                            url_suffix = ""
                            if parameters:
                                url_suffix = "?" + urllib.urlencode(parameters)
                            
                            headers[0] = method + " " + abs_path + url_suffix + " " + version
                        except:
                            self.stderr.println("error parameter: " + str(parameters))
                            self.stderr.println("error parameter: " + special_parameter)

            converted_headers = array.array('b', [ord(c) for c in "\r\n".join(headers)])
            message_info.setRequest(converted_headers + array.array('b', [ord(i) for i in "\r\n" * 3]) + request[request_info.getBodyOffset():] + array.array('b', [ord(i) for i in "\r\n" * 3]))
