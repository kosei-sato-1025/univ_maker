import pygame
import sys
import os
import json

# ファイルパスクラス
class FilePath:
    def __init__(self):
        self.base_path = os.path.dirname(__file__)
        self.mod_flag = False

    def is_there_mod(self, folder_path):
        mod_path = os.path.join(self.base_path, "mods", folder_path)
        if os.path.exists(mod_path) and self.mod_flag:
            return mod_path
        else:
            return os.path.join(self.base_path, folder_path)

# ゲームデータクラス
class GameData:
    def __init__(self, path):
        self.score = 0
        self.level = 1
        self.time = 0  # タイマー
        self.is_game_over = False
        self.save_folder = os.path.join(path.base_path, "saves")

    # ゲームの状態を保存するメソッド
    def save_game(self, file_name):
        if not os.path.exists(self.save_folder):
            os.makedirs(self.save_folder)
        file_path = os.path.join(self.save_folder, file_name)
        save_data = {
            "score": self.score,
            "level": self.level,
            "time": self.time,
            "is_game_over": self.is_game_over
        }
        with open(file_path, 'w') as f:
            json.dump(save_data, f, indent=4)  # データをjson形式で保存

    # 保存されたゲームの状態を読み込むメソッド
    def load_game(self, file_name):
        file_path = os.path.join(self.save_folder, file_name)
        try:
            with open(file_path, 'r') as f:
                save_data = json.load(f)
                self.score = save_data["score"]
                self.level = save_data["level"]
                self.time = save_data["time"]
                self.is_game_over = save_data["is_game_over"]
            return 1
        except Exception as e:
            return 0
    
    def get_save_files(self):
        # savesフォルダ内のjsonファイルをリスト化
        if not os.path.exists(self.save_folder):
            os.makedirs(self.save_folder)
        return [f for f in os.listdir(self.save_folder) if f.endswith('.json')]

    def reset_game(self):
        self.score = 0
        self.level = 1
        self.time = 0  # タイマー
        self.is_game_over = False

#言語データ設定クラス   
class Language:
    def __init__(self ,path):
        self.languages_folder =  path.is_there_mod("languages/language.json")

    # 言語設定メソッド
    def load_language(self):
        try:
            with open(self.languages_folder, 'r') as f:
                language_data = json.load(f)
                self.font = language_data["font"]
                self.title = language_data["Univ maker"]
                self.Start_Game = language_data["Start Game"]
                self.Start = language_data["Start"]
                self.Stop = language_data["Stop"]
                self.Press_ESC_to_go_back = language_data["Press ESC to go back"]
                self.Save_Data = language_data["Save Data"]
                self.Load_Data = language_data["Load Data"]
                self.Back_to_Start = language_data["Back to Start"]
                self.Select_a_saved_game = language_data["Select a saved game"]
                self.The_selected_file_may_be_in_a_different_format_or_corrupted = language_data["The selected file may be in a different format or corrupted"]
                self.error = language_data["error"]
                self.mod_ON = language_data["mod_ON"]
                self.mod_OFF = language_data["mod_OFF"]       
            return 1
        except Exception as e:
            print(f"{e}")
            return 0

# イメージオブジェクトクラス
class ImageObject:
    def __init__(self, image_path, color, text, text_color, font, x, y, width, height):
        self.image_path = image_path
        self.color = color
        self.text = text
        self.text_color = text_color
        self.font = font
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x - width//2, y - height//2, width, height)
        if(self.image_path != None):
            self.image = pygame.image.load(image_path)
            self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))

    def draw(self, screen):
        if(self.image_path != None):
            screen.blit(self.image, (self.rect.x, self.rect.y))
        elif(self.color != None):
            screen.fill(self.color, self.rect)
        text = self.font.render(self.text, True, self.text_color)
        screen.blit(text, (self.rect.x + ((self.rect.width-text.get_width())//2), self.rect.y + ((self.rect.height - text.get_height())//2)))

# 基底クラス: 画面
class Screen:
    def __init__(self, app):
        self.app = app

    def handle_event(self, event):
        pass

    def update(self):
        pass

    def draw(self):
        pass

# スタート画面クラス
class StartScreen(Screen):
    def __init__(self, app):
        super().__init__(app)
        self.app.data.reset_game()

        # 画像のパスを相対パスで指定
        background_path = self.app.path.is_there_mod("images/start_background.jpg")
        button_paper_path = self.app.path.is_there_mod("images/button_paper.jpg")
        title_path = self.app.path.is_there_mod("images/title.jpg")

        # 背景オブジェクトの設定
        self.backgronud = ImageObject(background_path, None, "", self.app.BLACK, self.app.font, self.app.width // 2, self.app.height // 2, self.app.width, self.app.height)

        # タイトルオブジェクトの設定
        self.title = ImageObject(title_path, None, self.app.language.title, self.app.BLACK, self.app.font, self.app.width // 2, self.app.height // 2 - 200, 300, 100)


        # ボタンオブジェクトの設定
        self.start_button = ImageObject(button_paper_path, None, self.app.language.Start, self.app.BLACK, self.app.font, self.app.width // 2, self.app.height // 2 - 100, 250, 50)
        self.load_button = ImageObject(button_paper_path, None, self.app.language.Load_Data, self.app.BLACK, self.app.font, self.app.width // 2, self.app.height // 2 , 250, 50)
        self.option_button = ImageObject(button_paper_path, None, self.app.language.Start, self.app.BLACK, self.app.font, self.app.width // 2, self.app.height // 2 + 100, 250, 50)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.start_button.rect.collidepoint(event.pos):
                self.app.change_screen(MainScreen(self.app))  # スタートボタン
            elif self.load_button.rect.collidepoint(event.pos):
                self.app.change_popup(LoadGamePopup(self.app))  # ロードボタン
            elif self.option_button.rect.collidepoint(event.pos):
                self.app.change_popup(OptionPopup(self.app))  # ロードボタン

    def draw(self):
        # 背景画像を描画
        self.backgronud.draw(self.app.screen)

        # タイトルを描画
        self.title.draw(self.app.screen)

        # ボタン画像を描画
        self.start_button.draw(self.app.screen)
        self.load_button.draw(self.app.screen)
        self.option_button.draw(self.app.screen)

# メイン画面クラス
class MainScreen(Screen):
    def __init__(self, app):
        super().__init__(app)
        self.button_rect = pygame.Rect(self.app.width // 2 - 100, self.app.height // 2 - 50, 200, 100)

        # 画像のパスを相対パスで指定
        background_path = self.app.path.is_there_mod("images/main_background.jpg")

        # 背景オブジェクトの設定
        self.backgronud = ImageObject(background_path, None, "", self.app.BLACK,  self.app.font, self.app.width // 2, self.app.height // 2, self.app.width, self.app.height)

        # タイマー関連
        self.timer_start = 0
        self.timer_running = False
        
        # タイマーオブジェクトの設定
        self.timerbox = ImageObject(None, self.app.GRAY, "", self.app.BLACK,  self.app.small_font, self.app.width // 2, self.app.height // 2, 200, 100)
        self.time  = ImageObject(None, None, "", self.app.BLACK,  self.app.small_font, self.timerbox.x , self.timerbox.y - 25, 100, 50)
        self.start_button = ImageObject(None, self.app.BLACK, self.app.language.Start, self.app.WHITE,  self.app.small_font, self.timerbox.x + 50, self.timerbox.y + 25, 100, 50)
        self.stop_button = ImageObject(None, self.app.BLACK, self.app.language.Stop, self.app.WHITE,  self.app.small_font, self.timerbox.x - 50, self.timerbox.y + 25, 100, 50)

        # メニューボタン群の設定
        self.bar = ImageObject(None, self.app.GRAY, "", self.app.WHITE,  self.app.small_font, 150, self.app.height//2, 300, self.app.height)
        self.construct_button = ImageObject(None, self.app.BLUE, self.app.language.Start_Game, self.app.WHITE,  self.app.small_font, self.bar.x, self.bar.y+100, 100, 50)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.construct_button.rect.collidepoint(event.pos):
                self.app.change_screen(ConstructionScreen(self.app))
            # タイマーボタンの処理
            if self.start_button.rect.collidepoint(event.pos):
                self.timer_start = pygame.time.get_ticks() - self.app.data.time
                self.timer_running = True
            elif self.stop_button.rect.collidepoint(event.pos):
                self.app.data.time = pygame.time.get_ticks() - self.timer_start
                self.timer_running = False
        
        # 小メニューを開く
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.app.change_popup(MainMenuPopup(self.app))               
            
    def update(self):
        if self.timer_running:
            self.app.data.time = pygame.time.get_ticks() - self.timer_start
        
        minutes = self.app.data.time // 60000
        seconds = (self.app.data.time // 1000) % 60
        self.time.text = f"{minutes:02}:{seconds:02}"

    def draw(self):
        # 背景画像を描画
        self.backgronud.draw(self.app.screen)

        # メニューバーの表示
        self.bar.draw(self.app.screen)
        self.construct_button.draw(self.app.screen)

        # タイマーの表示
        self.timerbox.draw(self.app.screen)
        self.time.draw(self.app.screen)
        self.start_button.draw(self.app.screen)
        self.stop_button.draw(self.app.screen)

# 建設画面クラス
class ConstructionScreen(Screen):
    def __init__(self, app):
        super().__init__(app)
        # 図形のリスト (位置と色を格納)
        self.shapes = [
            {"rect": pygame.Rect(100, 100, 100, 100), "color": self.app.RED},
            {"rect": pygame.Rect(300, 100, 100, 100), "color": self.app.BLUE},
            {"rect": pygame.Rect(500, 100, 100, 100), "color": self.app.GREEN},
        ]
        self.selected_shape = None
        self.offset_x, self.offset_y = 0, 0

        # 戻り表示
        self.return_button = ImageObject(None, self.app.RED, "<-", self.app.WHITE,  self.app.small_font, 20, 20, 20, 20)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # 図形を選択
            for shape in self.shapes:
                if shape["rect"].collidepoint(event.pos):
                    self.selected_shape = shape
                    self.offset_x = shape["rect"].x - event.pos[0]
                    self.offset_y = shape["rect"].y - event.pos[1]
                    break
            if self.return_button.rect.collidepoint(event.pos):
                self.app.change_screen(MainScreen(self.app))

        elif event.type == pygame.MOUSEBUTTONUP:
            self.selected_shape = None
        elif event.type == pygame.MOUSEMOTION:
            if self.selected_shape:
                self.selected_shape["rect"].x = event.pos[0] + self.offset_x
                self.selected_shape["rect"].y = event.pos[1] + self.offset_y
        

        # ゲーム画面からメニューに戻る
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.app.change_popup(MainMenuPopup(self.app))

    def draw(self):
        self.app.screen.fill(self.app.WHITE)
        # 図形を描画
        for shape in self.shapes:
            pygame.draw.rect(self.app.screen, shape["color"], shape["rect"])

        self.return_button.draw(self.app.screen)

# 小画面の基底クラス
class Popup:
    def __init__(self, app):
        self.app = app
        self.rect = self.app.popup.get_rect(center=(400, 300))  # 中央に配置
        self.app.popup.fill(self.app.GRAY)  # 背景色

        # 閉じるボタン
        self.close_button = ImageObject(None, self.app.RED, "X", self.app.WHITE,  self.app.font, self.app.small_width - 40, 40, 50, 50)

    def draw(self):
        """小画面を描画"""
        self.app.screen.blit(self.app.popup, self.rect.topleft)
        # 閉じるボタンを描画
        self.close_button.draw(self.app.popup)

    def handle_event(self, event):
        """閉じるボタンのイベント処理"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.close_button.rect.collidepoint(event.pos[0] - self.rect.x, event.pos[1] - self.rect.y):
                self.app.change_popup(NullPopup(self.app))

# 何も表示しないポップアップクラス
class NullPopup(Popup):
    def __init__(self, app):
        super().__init__(app)

    def draw(self):
        pass

    def handle_event(self, event):
        pass

# メインメニューポップアップクラス
class MainMenuPopup(Popup):
    def __init__(self, app):
        super().__init__(app)

        # ボタンの定義
        self.save_button = ImageObject(None, self.app.WHITE, self.app.language.Save_Data, self.app.BLACK,  self.app.small_font, self.app.small_width//2, 50, 120, 40)
        self.load_button = ImageObject(None, self.app.WHITE, self.app.language.Load_Data, self.app.BLACK,  self.app.small_font, self.app.small_width//2, 150, 120, 40)
        self.back_button = ImageObject(None, self.app.WHITE, self.app.language.Back_to_Start, self.app.BLACK,  self.app.small_font, self.app.small_width//2, 250, 120, 40)


    def draw(self):
        """小画面を描画 (ボタン付き)"""
        super().draw()  # 基底クラスの描画を呼び出す

        # Save Data ボタン
        self.save_button.draw(self.app.popup)

        # Load Data ボタン
        self.load_button.draw(self.app.popup)

        # Back to Start Menu ボタン
        self.back_button.draw(self.app.popup)

    def handle_event(self, event):
        """ボタンのイベント処理"""
        super().handle_event(event)  # 基底クラスの閉じるボタン処理

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Save Data ボタンが押された場合
            if self.save_button.rect.collidepoint(event.pos[0] - self.rect.x, event.pos[1] - self.rect.y):
                # 必要に応じて実際のセーブ処理を実装
                self.app.change_popup(SaveGamePopup(self.app))

            # Load Data ボタンが押された場合
            if self.load_button.rect.collidepoint(event.pos[0] - self.rect.x, event.pos[1] - self.rect.y):
                # 必要に応じて実際のセーブ処理を実装
                self.app.change_popup(LoadGamePopup(self.app))

            # Back to Start Menu ボタンが押された場合
            elif self.back_button.rect.collidepoint(event.pos[0] - self.rect.x, event.pos[1] - self.rect.y):
                # スタートメニュー画面へ遷移
                self.app.change_screen(StartScreen(self.app))

# ロードメニューポップアップクラス
class LoadGamePopup(Popup):
    def __init__(self, app):
        super().__init__(app)
        self.file_list = self.app.data.get_save_files()
        self.selected_file = None
        self.file_rects = []  # ファイル名ごとに背景のRectを管理するリスト

        # ボタンの定義
        self.load_button = ImageObject(None, self.app.WHITE, self.app.language.Load_Data, self.app.BLACK,  self.app.small_font, self.app.small_width//2, self.app.small_height - 100, 120, 40)

        # ファイルの一覧の文言を表示
        self.text = ImageObject(None, None, self.app.language.Select_a_saved_game, self.app.BLACK,  self.app.small_font, self.app.small_width//2, 30, 120, 40)



    def handle_event(self, event):
        super().handle_event(event)  # 基底クラスの閉じるボタン処理

        # マウスクリックでファイル選択
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i, file_rect in enumerate(self.file_rects):
                if file_rect.collidepoint(event.pos[0] - self.rect.x, event.pos[1] - self.rect.y):
                    self.selected_file = self.file_list[i]

            # ロードボタンが押されたら
            if self.load_button.rect.collidepoint(event.pos[0] - self.rect.x, event.pos[1] - self.rect.y):
                if(self.selected_file != None):
                    if(self.app.data.load_game(self.selected_file)==1):
                        self.app.change_screen(MainScreen(self.app))  # メイン画面に遷移
                    else:
                        self.app.change_popup(ErrorPopup(self.app, self.app.language.The_selected_file_may_be_in_a_different_format_or_corrupted))

    def draw(self):
        super().draw()  # 基底クラスの描画を呼び出す

        # セーブファイルの一覧の文言の表示
        self.text.draw(self.app.popup)

        # ファイル名の背景とテキストを描画
        y_offset = 100  # リストの開始位置
        self.file_rects = []  # 再初期化

        for i, file_name in enumerate(self.file_list):
            file_y = y_offset + (i * 50)
            file_rect = pygame.Rect(50, file_y, self.app.small_width - 100, 40)

            # 選択中のファイルは色を変える
            if file_name == self.selected_file:
                pygame.draw.rect(self.app.popup, (150, 200, 255), file_rect)  # 選択中は青っぽい色
            else:
                pygame.draw.rect(self.app.popup, (220, 220, 220), file_rect)  # 通常時はグレー

            # 枠線を描画
            pygame.draw.rect(self.app.popup, self.app.BLACK, file_rect, 2)

            # ファイル名を描画
            file_text = self.app.small_font.render(os.path.splitext(file_name)[0], True, self.app.BLACK)
            self.app.popup.blit(file_text, (file_rect.x + 10, file_rect.y + 5))

            # ファイル名ごとに背景のRectを保存
            self.file_rects.append(file_rect)
        
        # load実行 ボタン
        self.load_button.draw(self.app.popup)

# セーブメニューポップアップクラス
class SaveGamePopup(Popup):
    def __init__(self, app):
        super().__init__(app)
        self.input_text = ""  # 入力中の文字列
        self.is_typing = False  # テキストボックスがアクティブかどうか

        # 入力ボックスの位置とサイズ
        self.input_box = pygame.Rect(100, 200, 400, 50)

        # 決定ボタンの位置とサイズ
        self.save_button = ImageObject(None, self.app.WHITE, self.app.language.Save_Data, self.app.BLACK, self.app.small_font, self.app.small_width//2, self.app.small_height - 100, 120, 40)

    def handle_event(self, event):
        super().handle_event(event)  # 閉じるボタン処理

        # 入力ボックスのクリック処理
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.input_box.collidepoint(event.pos[0] - self.rect.x, event.pos[1] - self.rect.y):
                self.is_typing = True  # テキスト入力をアクティブに
            else:
                self.is_typing = False  # 他をクリックしたら非アクティブに

            # 決定ボタンのクリック処理
            if self.save_button.rect.collidepoint(event.pos[0] - self.rect.x, event.pos[1] - self.rect.y):
                if(self.input_text!=""):
                    self.app.data.save_game(self.input_text+".json")
                    self.app.change_popup(NullPopup(self.app))  # ポップアップを閉じる

        # キーボード入力処理
        if event.type == pygame.KEYDOWN and self.is_typing:
            if event.key == pygame.K_RETURN:  # Enterキーで決定
                pass
            elif event.key == pygame.K_BACKSPACE:  # バックスペースで文字を削除
                self.input_text = self.input_text[:-1]
            else:  # その他の文字を追加
                self.input_text += event.unicode

    def draw(self):
        super().draw()  # 基底クラスの描画

        # 入力ボックスを描画
        pygame.draw.rect(self.app.popup, self.app.WHITE, self.input_box)  # 白い背景
        pygame.draw.rect(self.app.popup, self.app.BLACK, self.input_box, 2)  # 黒い枠線
        input_text_popup = self.app.small_font.render(self.input_text, True, self.app.BLACK)
        self.app.popup.blit(input_text_popup, (self.input_box.x + 10, self.input_box.y + 10))

        # 決定ボタンを描画
        self.save_button.draw(self.app.popup)

# エラーポップアップクラス
class ErrorPopup(Popup):
    def __init__(self, app, error_text):
        super().__init__(app)
        self.error_text = error_text
        self.title = ImageObject(None, self.app.WHITE, self.app.language.error, self.app.BLACK, self.app.small_font,  self.app.small_width//2, 50, 120, 40)
        self.error = ImageObject(None, self.app.WHITE, self.error, self.app.BLACK, self.app.small_font, self.app.small_width//2, 200, 120, 40)


    def draw(self):
        super().draw()

        # タイトルを表示
        self.title.draw(self.app.popup)
        self.error.draw(self.app.popup)

    def handle_event(self, event):
        super().handle_event(event)

# オプションメニューポップアップクラス
class OptionPopup(Popup):
    def __init__(self, app):
        super().__init__(app)

        # ボタンの定義
        self.mod_button = pygame.Rect(self.app.small_width//2 - 60, 50, 120, 40)  # mod ボタン
        self.display_mod_status()

    def draw(self):
        """小画面を描画 (ボタン付き)"""
        super().draw()  # 基底クラスの描画を呼び出す

        # mod ボタン
        pygame.draw.rect(self.app.popup, self.app.WHITE, self.mod_button)
        self.app.popup.blit(self.mod_text, (self.mod_button.x + 10, self.mod_button.y + 10))

    def handle_event(self, event):
        """ボタンのイベント処理"""
        super().handle_event(event)  # 基底クラスの閉じるボタン処理

        if event.type == pygame.MOUSEBUTTONDOWN:
            # mod ボタンが押された場合
            if self.mod_button.collidepoint(event.pos[0] - self.rect.x, event.pos[1] - self.rect.y):
                if(self.app.path.mod_flag):
                    self.app.path.mod_flag = False
                else:
                    self.app.path.mod_flag = True
                self.app.refresh()
        self.display_mod_status()

    def display_mod_status(self):
            if(self.app.path.mod_flag):
                self.mod_text = self.app.small_font.render(self.app.language.mod_ON, True, self.app.BLACK)
            else:
                self.mod_text = self.app.small_font.render(self.app.language.mod_OFF, True, self.app.BLACK)

# アプリケーションクラス
class App:
    def __init__(self):
        # 初期化
        pygame.init()

        # 色の定義
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (200, 200, 200)
        self.RED = (255, 0, 0)
        self.BLUE = (0, 0, 255)
        self.GREEN = (0, 255, 0)

        # ファイルパス設定
        self.path = FilePath()

        #言語設定
        self.config_language()

        # ウィンドウサイズ
        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))

        # ポップアップサイズ
        self.small_width = 600
        self.small_height = 500
        self.popup = pygame.Surface((self.small_width, self.small_height))  # 小画面のpopup

        self.data = GameData(self.path)
        self.current_screen = StartScreen(self)
        self.current_popup = NullPopup(self)

    def change_screen(self, new_screen):
        self.current_screen = new_screen
        self.change_popup(NullPopup(self))

    def change_popup(self, new_popup):
        self.current_popup = new_popup

    def config_language(self):
        # 言語設定
        self.language = Language(self.path)
        self.language.load_language()
        font_path = self.path.is_there_mod(f"languages/{self.language.font}")
        try:
            self.font = pygame.font.Font(font_path, 48)
        except Exception as e:
            print(f"{e}")
        try:
            self.small_font = pygame.font.Font(font_path, 24)
        except Exception as e:
            print(f"{e}")
        
        # タイトル
        pygame.display.set_caption(self.language.title)

    def refresh(self):
        self.config_language()
        popup = self.current_popup
        self.change_screen(self.current_screen.__class__(self))
        self.change_popup(popup.__class__(self))

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if(isinstance(self.current_popup, NullPopup)):
                    self.current_screen.handle_event(event)
                self.current_popup.handle_event(event)

            if(isinstance(self.current_popup, NullPopup)):
                self.current_screen.update()
            self.current_screen.draw()
            self.current_popup.draw()
            pygame.display.flip()

# アプリの実行
if __name__ == "__main__":
    app = App()
    app.run()
