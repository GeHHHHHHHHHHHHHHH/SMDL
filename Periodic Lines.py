import pya

# 创建新的布局和单元
layout = pya.Layout()
layout.dbu = 0.001  # 设置数据库单位为微米
cell = layout.create_cell("Top")

# 创建图层
layer_index = layout.insert_layer(pya.LayerInfo(1, 0)) 

# 定义矩形1的参数
rect_width = 20 / layout.dbu  # 主矩形宽度
rect_height = 500 / layout.dbu  # 主矩形高度
rect_spacing = 260 / layout.dbu  # 主矩形之间的横向间距

# 定义引出横向矩形2的参数
lead_width = 240 / layout.dbu  # 横向长度
lead_height = 1.0 / layout.dbu  # 纵向高度
lead_gap = 1.0 / layout.dbu # 双边间距
lead_spacing = lead_height + 2 * lead_gap  # 单边间距

# 绘制矩形1.1
rect1 = pya.Box(0, 0, rect_width, rect_height)
cell.shapes(layer_index).insert(rect1)

# 绘制矩形1.2，位于第一个矩形的右侧
rect2_x = rect_width + rect_spacing
rect2 = pya.Box(rect2_x, 0, rect2_x + rect_width, rect_height)
cell.shapes(layer_index).insert(rect2)

# 在第一个矩形的右侧面引出横向矩形2.1
y_position_left = 0
while y_position_left + lead_height <= rect_height:
    lead_rect1 = pya.Box(rect_width, y_position_left, rect_width + lead_width, y_position_left + lead_height)
    cell.shapes(layer_index).insert(lead_rect1)
    y_position_left += lead_height + lead_spacing

# 在第二个矩形的左侧面引出横向矩形2.2，起始位置偏移
y_position_right = lead_height + lead_gap   # 偏移
while y_position_right + lead_height <= rect_height:
    lead_rect2 = pya.Box(rect2_x - lead_width, y_position_right, rect2_x, y_position_right + lead_height)
    cell.shapes(layer_index).insert(lead_rect2)
    y_position_right += lead_height + lead_spacing

# 添加小矩形3
small_rect_height = 100 / layout.dbu  # 小矩形高度

# 矩形3.1
small_rect1 = pya.Box(0, -small_rect_height, rect_width, 0)
cell.shapes(layer_index).insert(small_rect1)

# 矩形3.2
small_rect2 = pya.Box(rect2_x, -small_rect_height, rect2_x + rect_width, 0)
cell.shapes(layer_index).insert(small_rect2)

# 添加梯形
trapezoid_height = 60 / layout.dbu  # 梯形高度，100 微米
trapezoid_bottom_width = 100 / layout.dbu  # 梯形下边宽度

# 第一个梯形
trapezoid1_top_left = (0, -small_rect_height)  # 上边的左端点
trapezoid1_top_right = (rect_width, -small_rect_height)  # 上边的右端点
trapezoid1_bottom_left = ((rect_width - trapezoid_bottom_width * 0.4) / 2, -small_rect_height - trapezoid_height)
trapezoid1_bottom_right = ((rect_width + trapezoid_bottom_width * 1.6) / 2, -small_rect_height - trapezoid_height)

# 四边形方法
polygon1 = pya.Polygon([pya.Point(*trapezoid1_top_left), pya.Point(*trapezoid1_top_right),
                        pya.Point(*trapezoid1_bottom_right), pya.Point(*trapezoid1_bottom_left)])
cell.shapes(layer_index).insert(polygon1)

# 第二个梯形
trapezoid2_top_left = (rect2_x, -small_rect_height)
trapezoid2_top_right = (rect2_x + rect_width, -small_rect_height)
trapezoid2_bottom_left = (rect2_x + (rect_width - trapezoid_bottom_width * 1.6) / 2, -small_rect_height - trapezoid_height)
trapezoid2_bottom_right = (rect2_x + (rect_width + trapezoid_bottom_width * 0.4) / 2, -small_rect_height - trapezoid_height)

# 四边形方法
polygon2 = pya.Polygon([pya.Point(*trapezoid2_top_left), pya.Point(*trapezoid2_top_right),
                        pya.Point(*trapezoid2_bottom_right), pya.Point(*trapezoid2_bottom_left)])
cell.shapes(layer_index).insert(polygon2)

# 添加矩形4到梯形的下方，横向宽度与梯形底边对齐
rectangle_height = 150 / layout.dbu  # 矩形高度

# 矩形4.1
rect1_bottom_x_left = trapezoid1_bottom_left[0]
rect1_bottom_x_right = trapezoid1_bottom_right[0]
rect1_y_bottom = trapezoid1_bottom_left[1] - rectangle_height

rectangle1 = pya.Box(rect1_bottom_x_left, rect1_y_bottom, rect1_bottom_x_right, trapezoid1_bottom_left[1])
cell.shapes(layer_index).insert(rectangle1)

# 矩形4.2
rect2_bottom_x_left = trapezoid2_bottom_left[0]
rect2_bottom_x_right = trapezoid2_bottom_right[0]
rect2_y_bottom = trapezoid2_bottom_left[1] - rectangle_height

rectangle2 = pya.Box(rect2_bottom_x_left, rect2_y_bottom, rect2_bottom_x_right, trapezoid2_bottom_left[1])
cell.shapes(layer_index).insert(rectangle2)

# save,默认为软件安装路径
layout.write("test.gds")
