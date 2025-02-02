import random
from game import Game
from chip import Chip
from monster import Monster
from monsterlist import MonsterList
# フィールドクラス（マップの１画面分のクラス）
class Field:
    mapnumber = 1
    # 関数：コンストラクタ
    def __init__(self):
        # Ａ－１９Chipから）フィールドのチップのリスト
        self.chip_list = None
        # Ａ－２０）マップ番号に初期値を設定
        self.map_no = Game.START_FIELD
        
        # Ａ－２１）表示用のチップ（マス）の２重リストを作成
        self.chip_list = [[Chip() for _ in range(Game.FIELD_WIDTH)] \
                           for _ in range(Game.FIELD_HEIGHT)]
        # Ａ－２２）チップリストの数だけ２重ループ
        for y in range(Game.FIELD_HEIGHT):
            for x in range(Game.FIELD_WIDTH):
                # Ａ－２３）位置と初期画像を指定
                self.chip_list[y][x].set_pos(x, y)
                self.chip_list[y][x].set_chip_no(0)
        # Ｂ－２８最初）マップ番号に対応した情報を設定
        self.read_map_info()

    # 描画をする
    def draw(self):
        # Ａ－２４）チップリストの数だけ２重ループ
        for y in range(Game.FIELD_HEIGHT):
            for x in range(Game.FIELD_WIDTH):
                # Ａ－２５mainへ）そのチップの描画をする
                self.chip_list[y][x].draw()
        
    # フィールド情報の読み込み
    def read_map_info(self):
        # Ｂ－２９）フィールド情報の設定
        new_field = Field.MAP_LIST[self.map_no]
        # Ｂ－３０）チップリストの数だけ２重ループ
        for y in range(Game.FIELD_HEIGHT):
            for x in range(Game.FIELD_WIDTH):
                # Ｂ－３１最後）フィールドの該当位置の情報を設定
                self.chip_list[y][x].set_chip_no(new_field[y][x])

    # フィールドチェンジ
    # （移動方向をfld_x, fld_yのプラスマイナス１でもらう）
    def change_field(self, fld_x, fld_y):
        Field.mapnumber = self.map_no
        # マップ数
        map_count = Game.MAP_COUNT
        # Ｆ－６１）左右移動後の位置がそのまま計算すると
        # 上下のフィールドになってしまう場合は、
        # １始まりなので１を引いてから割って比較）
        if (self.map_no - 1) // Game.MAP_WIDTH != \
           (self.map_no + fld_x - 1) // Game.MAP_WIDTH:
            # Ｆ－６２）フィールドの横の数－１だけ、逆方向に移動
            self.map_no += (Game.MAP_WIDTH - 1) * (fld_x * -1)
        # Ｆ－６３）そうでない場合
        else:
            # Ｆ－６４）マップNoを指定値加算
            self.map_no += fld_x
        
        # Ｆ－６５）上下に移動した場合は「横マップ数」を足す／引く
        self.map_no += fld_y * Game.MAP_WIDTH

        # Ｆ－６６）フィールド数を超えた場合は、マップ数を引く
        if self.map_no > map_count:
            self.map_no -= map_count
        # Ｆ－６７）０以下になった場合は、マップ数を足す
        elif self.map_no <= 0:
            self.map_no += map_count
        # Ｆ－６８Playerへ）フィールド情報を再読み込み
        self.read_map_info()
        
        # Ｊ－１２６Squareから）モンスターの再配置
        for monster in Game.monsters:                  
            # Ｊ－１２７）マスのピッタリの位置に配置する
            dx, dy = 0, 0
            # Ｊ－１２８）配置できるまでループする
            # （※無限ループしてしまわないように、100回で諦める）
            for _ in range(100):
                # Ｊ－１２９）プレイヤーが端からくるので、外側の２マスには配置しない
                posx = random.randint(2, Game.FIELD_WIDTH - 3)
                posy = random.randint(2, Game.FIELD_HEIGHT - 3)
                # Ｊ－１３０）モンスターが移動できない位置に配置されてしまった場合はやり直し
                if not monster.check_chara_move(posx, posy, dx, dy,
                                                monster.unmovable_chips):
                    continue
                # Ｊ－１３１Monsterへ）移動できる位置ならそこに配置
                monster.set_pos(posx, posy)
                monster.set_dpos(dx, dy)
            
                
    # 移動可能チェック
    def check_movable(self, pos_list, unmovable_chip_list):
        # Ｇ－８２最初）チェック対象だけ繰り返し
        for pos in pos_list:
            # Ｇ－８３）位置のx, yを取得
            x, y = pos[0], pos[1]
            # Ｇ－８４）その位置のチップNoを取得
            chip_no = self.chip_list[y][x].chip_no
            # Ｇ－８５）それが移動不可ならFalseを返却
            if chip_no in unmovable_chip_list:
                return False
        # Ｇ－８６Characterへ）すべての対象チップが移動可能な場合はTrueを返却
        return True
    # 毒の沼
    def check_filed_damege(self, pos_list, filed_damege_list):
        # Ｇ－８２最初）チェック対象だけ繰り返し
        for pos in pos_list:
            # Ｇ－８３）位置のx, yを取得
            x, y = pos[0], pos[1]
            # Ｇ－８４）その位置のチップNoを取得
            chip_no = self.chip_list[y][x].chip_no
            if chip_no in filed_damege_list:
                return False
                
        # Ｇ－８６Characterへ）すべての対象チップが移動可能な場合はTrueを返却
        return True
# 宝箱
    def check_filed_takarabako(self, pos_list, filed_takarabako_list):
        # Ｇ－８２最初）チェック対象だけ繰り返し
        for pos in pos_list:
            # Ｇ－８３）位置のx, yを取得
            x, y = pos[0], pos[1]
            # Ｇ－８４）その位置のチップNoを取得
            chip_no = self.chip_list[y][x].chip_no
            if chip_no in filed_takarabako_list:
                return False
                
        # Ｇ－８６Characterへ）すべての対象チップが移動可能な場合はTrueを返却
        return True
# 落とし物
    def check_filed_otoshimono(self, pos_list, filed_otoshimono_list):
        # Ｇ－８２最初）チェック対象だけ繰り返し
        for pos in pos_list:
            # Ｇ－８３）位置のx, yを取得
            x, y = pos[0], pos[1]
            # Ｇ－８４）その位置のチップNoを取得
            chip_no = self.chip_list[y][x].chip_no
            if chip_no in filed_otoshimono_list:
                return False
                
        # Ｇ－８６Characterへ）すべての対象チップが移動可能な場合はTrueを返却
        return True    
# ドア
    def check_filed_door(self, pos_list, filed_door_list):
        # Ｇ－８２最初）チェック対象だけ繰り返し
        for pos in pos_list:
            # Ｇ－８３）位置のx, yを取得
            x, y = pos[0], pos[1]
            # Ｇ－８４）その位置のチップNoを取得
            chip_no = self.chip_list[y][x].chip_no
            if chip_no in filed_door_list:
                return False
                
        # Ｇ－８６Characterへ）すべての対象チップが移動可能な場合はTrueを返却
        return True    
    

    # クラス変数：マップ情報
    MAP1 = (
        (3,3,3,0,0,0,0,2,0,2),
        (3,0,0,0,1,1,0,2,0,2), 
        (3,0,0,0,0,1,0,2,0,2), 
        (3,0,0,0,0,1,0,2,2,2), 
        (3,0,0,0,0,1,4,4,4,4), 
        (3,0,0,0,0,1,0,4,4,4), 
        (3,0,0,0,0,1,4,4,4,4), 
        (3,0,3,0,1,1,1,4,4,4), 
        (3,3,3,3,0,4,4,4,4,4), 
        (3,0,3,3,3,3,3,3,3,3) 
    )
    MAP2 = [
        (2,2,2,2,2,2,2,2,2,2), 
        (2,4,4,4,4,4,4,0,0,2), 
        (2,4,4,4,3,4,4,3,0,2), 
        [2,4,4,3,3,4,4,0,5,2], 
        (4,4,4,3,3,4,4,0,0,2), 
        (4,4,4,4,3,4,4,4,4,2), 
        (4,4,4,4,3,4,4,4,4,2), 
        (4,4,4,4,4,3,4,4,4,2), 
        (4,4,4,4,4,4,4,1,3,2), 
        (2,2,2,2,2,2,2,2,2,2)
    ]
    MAP3 = (
        (2,0,0,0,0,0,0,0,0,2), 
        (2,0,0,1,1,1,1,0,0,2), 
        (2,0,1,0,0,0,0,1,0,2), 
        (2,0,0,0,0,0,0,1,0,2), 
        (2,0,0,0,0,0,1,0,0,2), 
        (2,0,0,0,0,0,0,1,0,2), 
        (2,0,1,0,0,0,0,1,0,2), 
        (2,0,0,1,1,1,1,0,0,2), 
        (2,0,0,0,0,0,0,0,0,2), 
        (2,3,3,3,2,2,0,0,0,2)
    )
    MAP4 = (
        (0,0,3,3,3,0,0,0,0,0), 
        (0,0,0,0,0,0,0,0,0,3), 
        (10,11,11,10,10,10,10,10,10,10), 
        (2,2,2,2,2,2,2,2,2,2), 
        (2,2,2,2,2,2,2,2,2,2), 
        (2,2,2,2,2,2,2,2,2,2), 
        (2,2,2,2,2,2,2,2,2,2), 
        (3,3,3,3,3,3,3,3,3,3), 
        (3,3,3,3,3,3,3,3,3,3), 
        (3,3,3,3,3,3,3,3,3,3)
    )
    MAP5 = [
        (0,2,2,0,0,0,0,0,0,3), 
        (3,0,0,0,0,0,0,0,0,0), 
        (10,10,10,10,10,10,10,10,10,10), 
        (2,2,2,2,2,2,2,2,2,2), 
        (2,2,2,2,2,2,2,2,2,2), 
        (2,2,2,2,2,2,2,2,2,2), 
        (2,2,2,2,2,2,2,2,2,2), 
        (3,3,3,3,3,3,3,3,3,3), 
        (3,3,3,3,3,3,3,3,3,3), 
        (3,3,3,3,3,3,3,3,3,3)
    ]
    MAP6 = (
        (2,3,2,2,2,2,0,0,0,0), 
        (2,0,0,1,1,1,1,0,0,0), 
        (10,10,10,10,10,10,10,10,10,10), 
        (2,2,2,2,2,2,2,2,2,2), 
        (2,2,2,2,2,2,2,2,2,2), 
        (2,2,2,2,2,2,2,2,2,2), 
        (2,2,2,2,2,2,2,2,2,2), 
        (3,3,3,3,3,3,3,3,3,3), 
        (3,3,3,3,3,3,3,3,3,3), 
        (3,3,3,3,3,3,3,3,3,3)
    )
    MAP7 = (
        (2,2,2,2,2,2,2,2,2,2), 
        (0,0,0,0,0,0,0,0,0,0), 
        (0,0,1,1,1,1,1,0,0,0), 
        (0,0,1,0,0,0,1,0,0,0), 
        (0,0,0,0,0,0,1,0,0,0), 
        (0,0,0,0,0,0,1,0,0,0), 
        (0,0,0,0,0,1,0,0,0,0), 
        (0,0,0,0,0,1,0,0,0,0), 
        (0,0,0,0,1,0,0,0,0,0), 
        (3,3,3,0,0,0,0,2,2,3)
    )
    MAP8 = [
        (2,2,2,2,2,2,2,2,2,2), 
        (3,2,0,0,0,0,0,0,0,2), 
        (3,2,0,1,1,1,0,0,0,2), 
        (3,2,0,1,0,1,0,0,0,2), 
        [3,7,0,1,1,6,0,0,0,2], 
        [3,7,0,1,0,1,0,0,0,2], 
        (3,2,0,1,1,1,0,0,0,2), 
        (3,2,0,0,0,0,0,0,0,2), 
        (3,2,0,0,0,0,0,0,0,2), 
        (2,2,2,2,2,2,2,2,2,2) 
    ]
    MAP9 = (
        (2,2,2,2,2,2,2,2,2,2), 
        (2,0,0,0,0,0,0,0,0,0), 
        (2,0,4,1,4,4,0,0,0,0), 
        (2,4,4,4,0,4,4,0,0,0), 
        (2,4,4,1,1,1,4,0,0,0), 
        (2,4,0,0,0,1,4,0,0,0), 
        (2,0,4,0,0,4,4,0,0,0), 
        (2,3,4,4,4,4,0,0,0,0), 
        (2,3,3,3,4,4,0,0,0,0), 
        (2,0,0,0,0,0,0,0,0,3) 
    )

    MAP_LIST = (0, MAP1, MAP2, MAP3, MAP4, MAP5, MAP6, MAP7, MAP8, MAP9)
