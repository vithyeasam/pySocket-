import serial
import time
import eventlet
import socketio
import json 


sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio)
# , static_files= {
#     '/': {'content_type': 'text/html', 'filename': 'index.html'}
# })

ser = serial.Serial()  # open serial port
ser.baudrate = 9600 
ser.port = 'COM14'
text = ""

ser.open()
print(ser.is_open)
print('Open ' + ser.name)         # check which port was really used
    # ser.write(b'hello')     # write a string
    # ser.close()   


def bg_emit():
    sio.emit('my message', dict(foo='bar'))

def listen():
    msg = ser.read().decode()
    while True:
        text = ''
        while (msg != '\n'):
            if msg == '{':
                break
            # if len(msg) != 0: 
            elif msg != '}':
                text += msg         
            elif msg == '}':
                text += msg
                newText = '{' + text
                # print(newText)
                jsonText = json.loads(newText)
                print(jsonText)
                # print(json.dumps(text))
                sio.emit('my message', jsonText)
                    # time.sleep(2)
                    # print(text)
                # bg_emit()
                eventlet.sleep(2)
            msg = ser.read().decode() 
            # print(msg)
                        # print(text)
        msg = ''
        text= ''
        # bg_emit()
        # eventlet.sleep(5)
        # sio.emit('my message', 'hello there')

    # eventlet.wsgi.server(eventlet.listen(('127.0.0.1', 3000)), app)
# while (1): 
#             # sio.emit('my message', 'helll')
#     text = ''
#     while (msg != '\n'):
#                 # if msg == '{':
#         text += msg
#         if msg == '}':
#             print(text)
#                 # print('message will send')
#                 # sio.emit('my message', text)
#                 # time.sleep(2)
#                 # print(text)
#         msg = ser.read().decode() 
#                     # print(text)
            

#     msg = ''
            # text = ''
            
        # while 1: 
        #     bytes = ser.readline()
        #     time.sleep(0.01)
        #     print (bytes)


        # ser.close()

@sio.event
def connect(sid, environ):
    print('connect ', sid)
            # print('message will send')
            # sio.emit('my message', text)
            # eventlet.sleep(2)
    # sys.stdout.flush()
# @sio.on('connect')
# def send_data(topic, data):
#     sio.emit('my message', text)
#     eventlet.sleep(2)
@sio.event
def my_message(sid, data):
    print('message ', data)
        # sio.emit('test event', {'data': 'foobar'})
@sio.event
def disconnect(sid):
    print('disconnect ', sid)


eventlet.spawn(listen)

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('127.0.0.1', 3000)), app)

# sys.stdout.flush()
ser.close()


# ser.close()

# # do_close = False
# # while ser.open() and do_close is False: 
# #     print(ser.is_open())
# #     print(ser.readline())
# #     time.sleep(0.1)
# # ser.close()