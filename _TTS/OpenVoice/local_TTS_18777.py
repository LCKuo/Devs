import os
import torch
from openvoice import se_extractor
from openvoice.api import BaseSpeakerTTS, ToneColorConverter
from pydub import AudioSegment
from pydub.playback import play
import socket

####
device="cuda:0" if torch.cuda.is_available() else "cpu"
output_dir = 'outputs'

ckpt_converter = 'checkpoints/converter'
tone_color_converter = ToneColorConverter(f'{ckpt_converter}/config.json', device=device)
tone_color_converter.load_ckpt(f'{ckpt_converter}/checkpoint.pth')

reference_speaker = 'resources/demo_speaker1.mp3'  # This is the voice you want to clone
target_se, audio_name = se_extractor.get_se(reference_speaker, tone_color_converter, target_dir='processed', vad=True)

####

ckpt_base = 'checkpoints/base_speakers/ZH'
base_speaker_tts = BaseSpeakerTTS(f'{ckpt_base}/config.json', device=device)
base_speaker_tts.load_ckpt(f'{ckpt_base}/checkpoint.pth')

source_se = torch.load(f'{ckpt_base}/zh_default_se.pth').to(device)
save_path = f'{output_dir}/output_chinese.wav'
####


def generate_voice(text, speaker='default', language='Chinese', speed=1.0):
    # Run the base speaker tts
    src_path = f'{output_dir}/tmp.wav'
    base_speaker_tts.tts(text, src_path, speaker=speaker, language=language, speed=speed)

    if False :#變聲器
        output_path  = f'{output_dir}/output_chineseTra.wav'
        # Run the tone color converter 
        encode_message = "@MyShell"
        tone_color_converter.convert(
            audio_src_path=src_path, 
            src_se=source_se, 
            tgt_se=target_se, 
            output_path=output_path,
            message=encode_message)
        
    audio = AudioSegment.from_wav(src_path)
    play(audio)


def start_server():
    # 創建一個 TCP/IP 伺服器
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 綁定伺服器到指定的端口
    server_address = ('localhost', 18777)
    print('Starting server on %s port %s' % server_address)
    server_socket.bind(server_address)

    # 監聽連接
    server_socket.listen(1)

    while True:
        # 等待連接
        print('Waiting for a connection...')
        connection, client_address = server_socket.accept()

        try:
            print('Connection from', client_address)

            while True:
                # 接收字串
                data = connection.recv(1024).decode().strip()
                if not data:
                    break  # 如果沒有接收到資料，則退出循環

                print('Received:', data)
                generate_voice(data)

        finally:
            # 關閉連接
            connection.close()



if __name__ == '__main__':
    start_server()