# Copyright (c) 2012-2014 Jonathan Warren
# Copyright (c) 2012-2014 The Bitmessage developers

from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler
import json

import shared
import time
from addresses import decodeVarint
import traceback

# Classes
from helper_sql import sqlQuery
from debug import logger

class APIError(Exception):
    def __init__(self, error_number, error_message):
        super(APIError, self).__init__()
        self.error_number = error_number
        self.error_message = error_message
    def __str__(self):
        return "API Error %03i: %s" % (self.error_number, self.error_message)

class MySimpleXMLRPCRequestHandler(SimpleXMLRPCRequestHandler):

    '''' The maximum size of a payload that we will return to a client, in bytes. '''
    MAX_PAYLOAD_SIZE_TO_RETURN = 256000
    
    def do_POST(self):
        # Handles the HTTP POST request.
        # Attempts to interpret all HTTP POST requests as XML-RPC calls,
        # which are forwarded to the server's _dispatch method for handling.

        # Note: this method is the same as in SimpleXMLRPCRequestHandler,
        # just hacked to handle cookies

        # Check that the path is legal
        if not self.is_rpc_path_valid():
            self.report_404()
            return

        try:
            # Get arguments by reading body of request.
            # We read this in chunks to avoid straining
            # socket.read(); around the 10 or 15Mb mark, some platforms
            # begin to have problems (bug #792570).
            max_chunk_size = 10 * 1024 * 1024
            size_remaining = int(self.headers["content-length"])
            L = []
            while size_remaining:
                chunk_size = min(size_remaining, max_chunk_size)
                L.append(self.rfile.read(chunk_size))
                size_remaining -= len(L[-1])
            data = ''.join(L)

            # In previous versions of SimpleXMLRPCServer, _dispatch
            # could be overridden in this class, instead of in
            # SimpleXMLRPCDispatcher. To maintain backwards compatibility,
            # check to see if a subclass implements _dispatch and dispatch
            # using that method if present.
            response = self.server._marshaled_dispatch(data, getattr(self, '_dispatch', None))
        except Exception,e:
            print str(e)
            print traceback.format_exc()
            # This should only happen if the module is buggy
            # internal error, report as HTTP server error
            self.send_response(500)
            self.end_headers()
        else:
            # got a valid XML RPC response
            self.send_response(200)
            self.send_header("Content-type", "text/xml")
            self.send_header("Content-length", str(len(response)))

            # HACK :start -> sends cookies here
            if self.cookies:
                for cookie in self.cookies:
                    self.send_header('Set-Cookie', cookie.output(header=''))
            # HACK :end

            self.end_headers()
            self.wfile.write(response)

            # shut down the connection
            self.wfile.flush()
            self.connection.shutdown(1)

    def APIAuthenticateClient(self):
        if 'Authorization' in self.headers:
            # handle Basic authentication
            (enctype, encstr) = self.headers.get('Authorization').split()
            (emailid, password) = encstr.decode('base64').split(':')
            if emailid == shared.config.get('bitmessagesettings', 'apiusername') and password == shared.config.get('bitmessagesettings', 'apipassword'):
                return True
            else:
                return False
        else:
            logger.warn('Authentication failed because header lacks Authentication field')
            time.sleep(2)
            return False

        return False

    def _decode(self, text, decode_type):
        try:
            return text.decode(decode_type)
        except Exception as e:
            raise APIError(1, "Decode error - " + str(e) + ". Had trouble while decoding string: " + repr(text))

    def _dispatch(self, method, params):
        self.cookies = []
        validuser = self.APIAuthenticateClient()
        if not validuser:
            time.sleep(2)
            return "RPC Username or password incorrect or HTTP header lacks authentication at all."
        try:
            return self._handle_request(method, params)
        except APIError as e:
            return str(e)
        except Exception as e:
            logger.exception(e)
            return "API Error 0021: Unexpected API Failure - " + str(e) + ".\nFull stack trace: " + traceback.format_exc()
        
    def addPayloadToOutput(self, array, payload):
        array.append({'data':payload.encode('hex')})
        return array
    
    def addQueryReturnToOutput(self, output, queryReturn):
        for row in queryReturn:
            payload, = row
            if len(payload) <= self.MAX_PAYLOAD_SIZE_TO_RETURN:
                output = self.addPayloadToOutput(output, payload)
        return output
    
    def outputPayload(self, name, payload):
        output = self.addPayloadToOutput([], payload)
        return self.outputAsJSON(name, output)
    
    def outputQueryReturn(self, name, queryReturn):
        output = self.addQueryReturnToOutput([], queryReturn)
        return self.outputAsJSON(name, output)
    
    def outputAsJSON(self, name, array):
        return json.dumps({name : array}, indent=4, separators=(',', ': '))
    
    # Checks whether the correct number of parameters has been provided
    def checkParameters(self, params, number):
        if len(params) != number:
            raise APIError(0, 'I need %s parameters!' %number) 

    def _handle_request(self, method, params):
        
        if method == 'add':
            (a, b) = params
            return a + b

    #   Commands for disseminating msgs, getpubkeys, and pubkeys

        elif method == 'disseminateMsg': 
            self.checkParameters(params, 1)
            payload, = params 
            payloadBytes = payload.decode('hex') 
            if (shared.checkAndShareMsgWithPeers(payloadBytes) > 0):
                return 'Message disseminated successfully'
            else:
                return 'Message dissemination failed'

        elif method == 'disseminatePubkey': 
            self.checkParameters(params, 1)
            payload, = params 
            payloadBytes = payload.decode('hex') 
            if (shared.checkAndSharePubkeyWithPeers(payloadBytes) > 0):
                return 'Pubkey disseminated successfully'
            else:
                return 'Pubkey dissemination failed'

        elif method == 'disseminateGetpubkey': 
            self.checkParameters(params, 1)
            payload, = params 
            payloadBytes = payload.decode('hex') 
            if (shared.checkAndSharegetpubkeyWithPeers(payloadBytes) > 0):
                return 'Getpubkey disseminated successfully'
            else:
                return 'Getpubkey dissemination failed'


        #   Commands for requesting msgs and pubkeys

        elif method == 'requestPubkey': 
            if len(params) != 2: 
                raise APIError(0, 'I need 2 parameters!') 
            identifierHex, addressVersion = params # The identifier is either the ripe hash or the 'tag' of the pubkey we are requesting
            if addressVersion < 1:
                raise APIError(2, 'The address version cannot be less than 1')
            elif addressVersion > 4:
                raise APIError(3, 'Address versions above 4 are currently not supported')
            elif addressVersion < 4: # For pubkeys of address versions 1-3
                if len(identifierHex) != 40: 
                    raise APIError(4, 'The length of hash should be 20 bytes (encoded in hex and thus 40 characters).')
                else:
                    requestedHash = self._decode(identifierHex, "hex")
                    queryReturn = sqlQuery('''SELECT transmitdata FROM pubkeys WHERE hash = ? ; ''', requestedHash) 
                    if queryReturn == []:
                        return 'No pubkeys found'
                    else:
                        payload = queryReturn[0]
                        if len(payload) <= self.MAX_PAYLOAD_SIZE_TO_RETURN:
                            return self.outputQueryReturn("pubkeyPayload", queryReturn)
                        else:
                            raise APIError(6, 'The requested object was found, but its payload is above the maximum size limit. The size of the object payload is ' + str(len(payload)))                   
            else:  # For pubkeys of address version 4  
                if len(identifierHex) != 64: 
                    raise APIError(5, 'The length of tag should be 32 bytes (encoded in hex and thus 64 characters).') 
                else:
                    requestedTag = self._decode(identifierHex, "hex")
                    queryReturn = sqlQuery('''SELECT payload FROM inventory WHERE objecttype='pubkey' and tag=? ''', requestedTag) 
                    if queryReturn != []:
                        payload = queryReturn[0]
                        if len(payload) <= self.MAX_PAYLOAD_SIZE_TO_RETURN:
                            return self.outputQueryReturn("pubkeyPayload", queryReturn)
                        else:
                            raise APIError(6, 'The requested object was found, but its payload is above the maximum size limit. The size of the object payload is ' + str(len(payload)))                   
                    else:
                        # We had no success looking in the sql inventory. Let's look through the memory inventory.
                        with shared.inventoryLock:
                            for hash, storedValue in shared.inventory.items():
                                objectType, streamNumber, payload, receivedTime, tag = storedValue
                                if objectType == 'pubkey' and tag == requestedTag:
                                    if len(payload) <= self.MAX_PAYLOAD_SIZE_TO_RETURN:
                                        return self.outputPayload("pubkeyPayload", payload)
                                    else:
                                        raise APIError(6, 'The requested object was found, but its payload is above the maximum size limit. The size of the object payload is ' + str(len(payload)))
                                else:
                                    return 'No pubkeys found'
                                
        elif method == 'checkForNewMsgs':
            self.checkParameters(params, 3)
            streamNumber, receivedSinceTime, receivedBeforeTime = params
            queryReturn = sqlQuery('''SELECT payload FROM inventory WHERE objecttype='msg' and streamnumber=? and receivedtime>? and receivedtime<? ''', streamNumber, receivedSinceTime, receivedBeforeTime)
            output = []
            if queryReturn != []:
                output = self.addQueryReturnToOutput(output, queryReturn)
            # Now let us search through the objects stored in memory
            with shared.inventoryLock:
                for hash, storedValue in shared.inventory.items():
                    objectType, streamNumber, payload, receivedTime, tag = storedValue
                    if objectType == 'msg' and receivedTime > receivedSinceTime and receivedTime < receivedBeforeTime:
                        if len(payload) <= self.MAX_PAYLOAD_SIZE_TO_RETURN:
                            output = self.addPayloadToOutput(output, payload)
            if output == []:
                return 'No msgs found'
            else:
                return self.outputAsJSON('msgPayloads', output)
