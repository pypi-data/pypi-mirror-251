import subprocess
import os

languages=[
        "English-Spanish-French-German-Italian-Portuguese-Dutch-Swedish-Danish-Norwegian-Japanese",
        "Inglés-Español-Francés-Alemán-Italiano-Portugués-Holandés-Sueco-Danés-Noruego-Japonés",
        "Anglais-Espagnol-Français-Allemand-Italien-Portugais-Néerlandais-Suédois-Danois-Norvégien-Japonais",
        "Englisch-Spanisch-Französisch-Deutsch-Italienisch-Portugiesisch-Niederländisch-Schwedisch-Dänisch-Norwegisch-Japanisch",
        "Inglese-Spagnolo-Francese-Tedesco-Italiano-Portoghese-Olandese-Svedese-Danese-Norvegese-Giapponese",
        "Inglês-Espanhol-Francês-Alemão-Italiano-Português-Holandês-Sueco-Dinamarquês-Norueguês-Japonês",
        "Engels-Spaans-Frans-Duits-Italiaans-Portugees-Nederlands-Zweeds-Deens-Noors-Japans",
        "Engelska-Spanska-Franska-Tyska-Italienska-Portugisiska-Holländska-Svenska-Danska-Norska-Japanska",
        "Engelsk-Spansk-Fransk-Tysk-Italiensk-Portugisisk-Hollandsk-Svensk-Dansk-Norsk-Japansk",
        "Engelsk-Spansk-Fransk-Tysk-Italiensk-Portugisisk-Nederlandsk-Svensk-Dansk-Norsk-Japansk"
    ];


def get_word_by_index(sentence, index):
    words = sentence.split('-')

    if 0 <= index < len(words):
        return words[index]
    else:
        return ""


def close_process(process_name):
    try:
        subprocess.run(["taskkill", "/f", "/im", process_name], check=True, creationflags=subprocess.CREATE_NO_WINDOW)
        print("Community website https://voicetranslator.github.io")
    except subprocess.CalledProcessError as e:
        print("Community website https://voicetranslator.github.io")



def voice_translator(x1,x2):

    app_name="voicetranslator.exe"

    base_path = os.path.dirname(
            os.path.abspath(__file__)
        )
    app = os.path.join(base_path, app_name)
    
    close_process(app_name)
    
    input_dict={"en-US":0,"es-ES":1,"fr-FR":2,"de-DE":3,"it-IT":4,"pt-PT":5,"nl-NL":6,"sv-SE":7,"da-DK":8,"no-NO":9,"ja-JP":10}
    output_dict={"en-US":0,"es-ES":1,"fr-FR":2,"de-DE":3,"it-IT":4,"pt-PT":5,"nl-NL":6,"sv-SE":7,"da-DK":8,"no-NO":9}

    if x1 in input_dict:
        input_lang=str(input_dict[x1])
    else:
        print("Error: Please try one of the follow languages:")
        print("en-US,es-ES,fr-FR,de-DE,it-IT,pt-PT,nl-NL,sv-SE,da-DK,no-NO,ja-JP")
        return 0

    if x2 in output_dict:
        output_lang=str(output_dict[x2])
    else:
        print("Error: Please try one of the follow languages:")
        print("en-US,es-ES,fr-FR,de-DE,it-IT,pt-PT,nl-NL,sv-SE,da-DK,no-NO")
        return 0

    print(get_word_by_index(languages[output_dict[x2]],input_dict[x1])+" - "+languages[output_dict[x2]].split("-")[output_dict[x2]])

    print("Ready to translate desktop audio...")
        
    startup_info = subprocess.STARTUPINFO()
    startup_info.dwFlags = subprocess.STARTF_USESHOWWINDOW 
    startup_info.wShowWindow = subprocess.SW_HIDE
    process = subprocess.Popen(
        [
            app,
            input_lang,
            output_lang,
            "provided_by_voicetranslator_github_io"
        ],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        startupinfo=startup_info,
        text=True,
        encoding='utf-8'
    )

    off=0
    try:
        while True:
            line = process.stdout.readline()
                
            if not line:
                break

            print(line, end='')
            if "Library error:\n"==line:
                off=1


    finally:
        if off!=1:
            message_to_cpp = "finish_python_app"
            process.stdin.write(message_to_cpp)
            process.stdin.flush()
            flac_data, stderr = process.communicate()
            process.terminate()
            
    

    return 1



