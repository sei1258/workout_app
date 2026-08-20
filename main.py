import flet as ft
from datetime import datetime
from training_storage import load_training, save_training
def main(page: ft.Page):
    window_L1=ft.TextField(label="日時　例：2024-11-11のように半角英数字で入力")
    window_L1_error = ft.Text(
            "日時の入力が違います。例のような形で入力してください",
            color=ft.Colors.RED,
            visible=False,
        )
    window_L2=ft.TextField(label="きつさ(RPE)")
    window_L2_error = ft.Text(
            "入力が違います",
            color=ft.Colors.RED,
            visible=False,
        )
    window_L3=ft.TextField(label="種目",visible=True)
    window_L3_error = ft.Text(
            "入力が違います",
            color=ft.Colors.RED,
            visible=False,
        )
    window_R1=ft.TextField(label="回数",visible=True)
    window_R1_error = ft.Text(
            "入力が違います",
            color=ft.Colors.RED,
            visible=False,
        )
    window_R2=ft.TextField(label="セット数",visible=True)
    window_R2_error = ft.Text(
            "入力が違います",
            color=ft.Colors.RED,
            visible=False,
        )
    window_R3=ft.TextField(label="重量 kg",visible=True)
    window_R3_error = ft.Text(
            "入力が違います",
            color=ft.Colors.RED,
            visible=False,
        )
    page.scroll = ft.ScrollMode.AUTO
    submit_button = ft.ElevatedButton("追加")
    cancel_button = ft.TextButton(
            "キャンセル",
            visible=False,
        )
    training_type = ft.Dropdown(
        value="strength_weight",
        options=[
            ft.DropdownOption(
                key="strength_weight",
                text="筋トレ・外部重量",
            ),
            ft.DropdownOption(
                key="strength_bodyweight",
                text="筋トレ・自重",
            ),
            ft.DropdownOption(
                key="running",
                text="ランニング",
            ),
        ],
    
    )
    training_records = load_training()
    collapsed_dates = set()
    training_list = ft.Column()
    deleting_record_id = [None]
    editing_training_id=[None]

    max_id = max(
            (record["id"] for record in training_records if "id" in record),
            default=0,
        )

    data_changed = False

    for record in training_records:
        if "id" not in record:
            max_id += 1
            record["id"] = max_id
            data_changed = True

    if data_changed:
        save_training(training_records)

    def select_training(selected_type):
        
        #内部リセット
        window_L3.value = ""
        window_R1.value = ""
        window_R2.value = ""
        window_R3.value = ""
        #入力リストの表示変更
        if selected_type == "strength_weight":
            window_L3.label = "種目"
            window_L3.visible = True

            window_R1.label = "回数"
            window_R3.visible = True
            window_R2.label = "セット数"
            window_R3.label = "重量 kg"

        elif selected_type == "strength_bodyweight":
            window_L3.label = "種目"
            window_L3.visible = True

            window_R1.label = "回数"
            window_R2.label = "セット数"
            window_R3.visible = False

        elif selected_type == "running":
            window_L3.label = "距離 km"
            window_L3.visible = True

            window_R1.label = "走行時間 分"
            window_R3.visible = True
            window_R2.label = "休憩時間　分"
            window_R3.label = "ラップ数"

        page.update()

    

    def add_training(e):
        selected_type = training_type.value
        if training_records:
            new_id = max(record.get("id", 0) for record in training_records) + 1
        else:
            new_id = 1

        result = read_common_inputs()
        if result is None:
            return
        date_text, rpe = result
        
        if selected_type == "strength_weight":
            # try:
            event=window_L3.value.strip()
            if not event:
                window_L3_error.visible = True
                page.update()
                return
            # except ValueError:
            #     window_L3_error.visible=True
            #     page.update()
            #     return
            try:
                reps=int(window_R1.value)
            except ValueError:
                window_R1_error.visible=True
                page.update()
                return
            try:
                sets=int(window_R2.value)
            except ValueError:
                window_R2_error.visible=True
                page.update()
                return
            try:   
                weight=float(window_R3.value)
            except ValueError:
                window_R3_error.visible=True
                page.update()
                return

            if not ( 1<=rpe<=10 and reps>=1 and sets>=1 and weight>0):
                    
                    return
                
            training_records.append(
                {
                    "id":new_id,
                    "種類":selected_type,
                    "日時":date_text,
                    "RPE":rpe,
                    "種目":event,
                    "回数":reps,
                    "セット数":sets,
                    "重量":weight,
                }
            )
                

        elif selected_type == "strength_bodyweight":
            # try:
            event=window_L3.value.strip()
            if not event:
                window_L3_error.visible = True
                page.update()
                return
            # except ValueError:
            #     window_L3_error.visible=True
            #     page.update()
            #     return
            try:
                reps=int(window_R1.value)
            except ValueError:
                window_R1_error.visible=True
                page.update()
                return
            try:
                sets=int(window_R2.value)
            except ValueError:
                window_R2_error.visible=True
                page.update()
                return
            
                
            
            if not(1<=rpe<=10 and reps>=1 and sets>=1):
                return    
            training_records.append(
                {
                    "id":new_id,
                    "種類":selected_type,
                    "日時":date_text,
                    "RPE":rpe,
                    "種目":event,
                    "回数":reps,
                    "セット数":sets,
                    "重量":None,
                    
                }
            )
        elif selected_type == "running":
            try:
                distance=float(window_L3.value)
                
            except ValueError:
                window_L3_error.visible=True
                page.update()
                return
            try:
                run_time=float(window_R1.value)
            except ValueError:
                window_R1_error.visible=True
                page.update()
                return
            try:
                break_time=int(window_R2.value)
            except ValueError:
                window_R2_error.visible=True
                page.update()
                return
            try:
                laps=int(window_R3.value)
            except ValueError:
                window_R3_error.visible=True
                page.update()
                return
            if not (1<=rpe<=10 and distance>0 and run_time>0 and break_time>=0 and laps>=0):
                return
            training_records.append(
                {
                    "id":new_id,
                    "種類":selected_type,
                    "日時":date_text,
                    "RPE":rpe,
                    "種目":"ランニング",
                    "距離":distance,
                    "走行時間_分":run_time,
                    "休憩時間_分":break_time,
                    "ラップ数":laps,
                }
            )
        save_training(training_records)
        refresh_training_list()
        clear_training_fields()
        clear_errors()
        page.update()

    def read_common_inputs():
        try:
            date_text=window_L1.value.strip()
            datetime.strptime(date_text,"%Y-%m-%d")
        except ValueError:
            window_L1_error.visible=True
            page.update()
            return
        try:
            rpe=int(window_L2.value)
        except ValueError:
            window_L2_error.visible=True
            page.update()
            return
        return date_text, rpe


    def clear_errors():
        window_L1_error.visible = False
        window_L2_error.visible = False
        window_L3_error.visible = False
        window_R1_error.visible = False
        window_R2_error.visible = False
        window_R3_error.visible = False

    def clear_training_fields():
        window_L3.value = ""
        window_R1.value = ""
        window_R2.value = ""
        window_R3.value = ""
        
    #削除タスク
    def start_delete(e):
            record_id = e.control.data
            deleting_record_id[0] = record_id
            refresh_training_list()
    
    def cancel_delete(e):
            deleting_record_id[0] = None
            refresh_training_list()
    
    
    def confirm_delete(e):
            record_id = deleting_record_id[0]
            if editing_training_id[0] == record_id:
                finish_edit()
            if record_id is None:
                return
    
            for record in training_records:
                if record["id"] == record_id:
                    training_records.remove(record)
                    break
    
            #if editing_task_id[0] == task_id:
            #    finish_edit()
    
            deleting_record_id[0] = None
            save_training(training_records)
            refresh_training_list()

            #編集状態
    def start_edit(e):
        record_id = e.control.data
        training_type.disabled = True
        
        for record in training_records:
            if record["id"] == record_id:
                training_type.value = record["種類"]
                select_training(record["種類"])
                if record["種類"] == "strength_weight":
                        window_L1.value = record["日時"]
                        window_L2.value= record["RPE"]
                        window_L3.value=record["種目"]
                        window_R1.value=record["回数"]
                        window_R2.value=record["セット数"]
                        window_R3.value=record["重量"]
                        
                elif record["種類"] == "strength_bodyweight":
                    window_L1.value = record["日時"]
                    window_L2.value= record["RPE"]
                    window_L3.value=record["種目"]
                    window_R1.value=record["回数"]
                    window_R2.value=record["セット数"]
                                    
                                
                
                elif record["種類"] == "running":
                    window_L1.value = record["日時"]
                    window_L2.value= record["RPE"]
                    window_L3.value=record["距離"]
                    window_R1.value=record["走行時間_分"]
                    window_R2.value=record["休憩時間_分"]
                    window_R3.value=record["ラップ数"]
                editing_training_id[0] = record_id
                submit_button.text = "更新"
                submit_button.on_click = update_training
                cancel_button.visible = True
                page.update()
                return
    
    def update_training(e):
        selected_type = training_type.value        
        record_id= editing_training_id[0]
        
        for record in training_records:
            if record["id"] == record_id:
                # record["種類"]=training_type.value
                
                result = read_common_inputs()
                if result is None:
                    return
                date_text, rpe = result
        
                if selected_type == "strength_weight":
                    # try:
                    event=window_L3.value.strip()
                    if not event:
                        window_L3_error.visible = True
                        page.update()
                        return
                    # except ValueError:
                    #     window_L3_error.visible=True
                    #     page.update()
                    #     return
                    try:
                        reps=int(window_R1.value)
                    except ValueError:
                        window_R1_error.visible=True
                        page.update()
                        return
                    try:
                        sets=int(window_R2.value)
                    except ValueError:
                        window_R2_error.visible=True
                        page.update()
                        return
                    try:   
                        weight=float(window_R3.value)
                    except ValueError:
                        window_R3_error.visible=True
                        page.update()
                        return
        
                    if not ( 1<=rpe<=10 and reps>=1 and sets>=1 and weight>0):
                            return
        
                    
                            
                    record["種類"]=selected_type
                    record["日時"]=date_text
                    record["RPE"]=rpe
                    record["種目"]=event
                    record["回数"]=reps
                    record["セット数"]=sets
                    record["重量"]=weight
                        
                    
        
        
                elif selected_type == "strength_bodyweight":
                    # try:
                    event=window_L3.value.strip()
                    if not event:
                        window_L3_error.visible = True
                        page.update()
                        return
                    # except ValueError:
                    #     window_L3_error.visible=True
                    #     page.update()
                    #     return
                    try:
                        reps=int(window_R1.value)
                    except ValueError:
                        window_R1_error.visible=True
                        page.update()
                        return
                    try:
                        sets=int(window_R2.value)
                    except ValueError:
                        window_R2_error.visible=True
                        page.update()
                        return
        
        
        
                    if not(1<=rpe<=10 and reps>=1 and sets>=1):
                        return    
                    
                    record["種類"]=selected_type
                    record["日時"]=date_text
                    record["RPE"]=rpe
                    record["種目"]=event
                    record["回数"]=reps
                    record["セット数"]=sets
                    record["重量"]=None
        
                    
                elif selected_type == "running":
                    try:
                        distance=float(window_L3.value)
        
                    except ValueError:
                        window_L3_error.visible=True
                        page.update()
                        return
                    try:
                        run_time=float(window_R1.value)
                    except ValueError:
                        window_R1_error.visible=True
                        page.update()
                        return
                    try:
                        break_time=int(window_R2.value)
                    except ValueError:
                        window_R2_error.visible=True
                        page.update()
                        return
                    try:
                        laps=int(window_R3.value)
                    except ValueError:
                        window_R3_error.visible=True
                        page.update()
                        return
                    if not (1<=rpe<=10 and distance>0 and run_time>0 and break_time>=0 and laps>=0):
                        return
                    
                            
                    record["種類"]=selected_type
                    record["日時"]=date_text
                    record["RPE"]=rpe
                    record["種目"]="ランニング"
                    record["距離"]=distance
                    record["走行時間_分"]=run_time
                    record["休憩時間_分"]=break_time
                    record["ラップ数"]=laps
            
                
                
                break
    
        save_training(training_records)
        finish_edit()
        refresh_training_list()
        
        
                
    
    def finish_edit(e=None):
        editing_training_id[0] = None
        window_L1.value = ""
        window_L2.value= ""
        window_L3.value=""
        window_R1.value=""
        window_R2.value=""
        window_R3.value=""
        training_type.disabled = False
    
        submit_button.text = "追加"
        submit_button.on_click = add_training
        cancel_button.visible = False
        page.update()

    
    def toggle_date(e):
        date = e.control.data

        if date in collapsed_dates:
            collapsed_dates.remove(date)
            
        else:
            collapsed_dates.add(date)
            
        refresh_training_list()


    def refresh_training_list():
        training_list.controls.clear()
        grouped_records = {}
        for record in training_records:
            #日付ごとに分ける
            date = record["日時"]
        
            if date not in grouped_records:
                grouped_records[date] = []
        
            grouped_records[date].append(record)

        for date in sorted(grouped_records.keys(), reverse=True):
            
            date_records = ft.Column(
                visible=date not in collapsed_dates
            )

            for record in grouped_records[date]:
                training_card = create_training_card(record)
                date_records.controls.append(training_card)
            
                
            
            if date in collapsed_dates:
                icon = ft.Icons.KEYBOARD_ARROW_RIGHT
            else:
                icon = ft.Icons.KEYBOARD_ARROW_DOWN
            date_header = ft.Row([
                ft.Text(date),

                ft.IconButton(

                    
                    icon=icon,
                    data=date,
                    on_click=toggle_date,
                ),
            ])

            training_list.controls.append(date_header)
            training_list.controls.append(date_records)
        page.update()

    def create_training_card(record):
        is_deleting = record["id"] == deleting_record_id[0]
        if record["種類"]=="strength_weight":
        
            training_card = ft.Card(
            #タスクカード作成
                content=ft.Column(
                    [
                        ft.Text(f"日時：{record["日時"]}"), 
                        ft.Text(f"RPE：{record["RPE"]}"),
                        ft.Text(f"種目；{record["種目"]}"),
                        ft.Row([
                            ft.Text(f"回数：{record["回数"]}"),
                            ft.Text(f"セット数：{record["セット数"]}"),
                            ft.Text(f"重量：{record["重量"]}kg"),
                            ]
                            ),
                        ft.Row([
                            ft.IconButton(
                                icon=ft.Icons.EDIT,
                                data=record["id"],
                                on_click=start_edit,
                                visible=not is_deleting,
                            ),
        
                            # 通常時のゴミ箱
                            ft.IconButton(
                                icon=ft.Icons.DELETE,
                                data=record["id"],
                                on_click=start_delete,
                                visible=not is_deleting,
                            ),
        
                            # 削除確認中だけ表示
                            ft.Text(
                                "削除しますか？",
                                color=ft.Colors.RED,
                                visible=is_deleting,
                            ),
        
                            ft.TextButton(
                                "削除",
                                on_click=confirm_delete,
                                visible=is_deleting,
                            ),
        
                            ft.TextButton(
                                "キャンセル",
                                on_click=cancel_delete,
                                visible=is_deleting,
                            ),
                            ]
                            ),
                    ]
                )   
            )
        
        
        
        elif record["種類"]=="strength_bodyweight":
            training_card = ft.Card(
            #カード作成
                content=ft.Column(
                #コラム作成
                    [
                        ft.Text(f"日時：{record["日時"]}"),
                        ft.Text(f"RPE：{record["RPE"]}"),
                        ft.Text(f"{record["種目"]}"),
                        ft.Row([
                            ft.Text(f"回数：{record["回数"]}"),
                            ft.Text(f"セット数：{record["セット数"]}"),
                            ]
                            ),
                        ft.Row([
                            ft.IconButton(
                                icon=ft.Icons.EDIT,
                                data=record["id"],
                                on_click=start_edit,
                                visible=not is_deleting,
                            ),
        
                            # 通常時のゴミ箱
                            ft.IconButton(
                                icon=ft.Icons.DELETE,
                                data=record["id"],
                                on_click=start_delete,
                                visible=not is_deleting,
                            ),
        
                            # 削除確認中だけ表示
                            ft.Text(
                                "削除しますか？",
                                color=ft.Colors.RED,
                                visible=is_deleting,
                            ),
        
                            ft.TextButton(
                                "削除",
                                on_click=confirm_delete,
                                visible=is_deleting,
                            ),
        
                            ft.TextButton(
                                "キャンセル",
                                on_click=cancel_delete,
                                visible=is_deleting,
                            ),
                            ]
                            ),
                    ]
                )
            )
            
        
        elif record["種類"]=="running":
            training_card = ft.Card(
            #カード作成
                content=ft.Column(
                #コラム作成
                    [
                        ft.Text(f"日時：{record["日時"]}"),
                        ft.Text(f"RPE：{record["RPE"]}"),
                        ft.Text(f"距離：{record["距離"]}km"),
                        ft.Row([
                            ft.Text(f"走行時間：{record["走行時間_分"]}分"),
                            ft.Text(f"休憩時間：{record["休憩時間_分"]}分"),
                            ft.Text(f"ラップ数：{record["ラップ数"]}"),
                            ]
                            ),
                        ft.Row([
                            ft.IconButton(
                                icon=ft.Icons.EDIT,
                                data=record["id"],
                                on_click=start_edit,
                                visible=not is_deleting,
                            ),
        
                            # 通常時のゴミ箱
                            ft.IconButton(
                                icon=ft.Icons.DELETE,
                                data=record["id"],
                                on_click=start_delete,
                                visible=not is_deleting,
                            ),
        
                            # 削除確認中だけ表示
                            ft.Text(
                                "削除しますか？",
                                color=ft.Colors.RED,
                                visible=is_deleting,
                            ),
        
                            ft.TextButton(
                                "削除",
                                on_click=confirm_delete,
                                visible=is_deleting,
                            ),
        
                            ft.TextButton(
                                "キャンセル",
                                on_click=cancel_delete,
                                visible=is_deleting,
                            ),
                            ]
                            ),
                    ]
                )
            )
        return training_card

    def input_group(field, error):
        return ft.Column(
            [
                field,
                error,
            ],
            width=450,
        )
            
        
    training_type.on_select = lambda e: select_training(e.control.value)
    #外側でこれ単体でプルダウンがセレクトされたらユーザー関数動かすという意味
    submit_button.on_click = add_training
    cancel_button.on_click = finish_edit
    

    page.add(
        
        #一番上の段
    ft.Row(
        [
            input_group(window_L1, window_L1_error),
            input_group(window_R1, window_R1_error),
            training_type,
        ],
        spacing=15,
        vertical_alignment=ft.CrossAxisAlignment.START,
    ),

        #２段目
        ft.Row(
            [
                input_group(window_L2, window_L2_error),
                input_group(window_R2, window_R2_error),
                ft.Row([
                    submit_button,
                    cancel_button,
                ]),
            ],
            spacing=15,
            vertical_alignment=ft.CrossAxisAlignment.START,
        ),
            #３段目
        ft.Row(
            [
                input_group(window_L3, window_L3_error),
                input_group(window_R3, window_R3_error),
            ],
            spacing=15,
            vertical_alignment=ft.CrossAxisAlignment.START,
        ),
        
        ft.Divider(),
        ft.Container(
            content=training_list,
            expand=True,
        ),
        
    )
    refresh_training_list()
ft.run(main)