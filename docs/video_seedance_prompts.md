# Seedance 2.0 Prompts — IoT-Telematik-Plattform

## Verwendung

Jeder Shot hat einen JSON-Block mit EN + ZH Prompt.
**Direkt in Seedance 2.0 copy-pasten** — den EN-Prompt für englische Generation, den ZH-Prompt für chinesische.

Still-Bilder als First Frame hochladen (siehe `video_stills.md`), dann den passenden Prompt hier verwenden.

**Text-Overlays werden in Post-Production ergänzt** (siehe unten).

---

## Shot 1.1 — Totale Autobahn, Drohne nähert sich

> First Frame: Still 1.1

```json
[{"lang":"en","prompt":"Style & Mood: Blue hour dusk, desaturated teal-and-steel palette with selective warm orange (#E67E22) from tail lights. Anamorphic lens, shallow depth of field, 24fps film grain. Wet asphalt shimmer, muted atmospheric haze. Corporate documentary tone. Dynamic Description: High-angle aerial drone descending toward a six-lane German Autobahn. The camera tilts from steep bird's-eye gradually flattening as it drops closer. Below, dense mixed traffic moves in both directions — white curtainside semi-trailers, refrigerated box trailers, sedans, SUVs. Red tail lights streak left-to-right in the near lanes, white headlights flow right-to-left opposite. The highway curves gently to the right. The descent is smooth and continuous, the ground growing larger, lane markings becoming distinct, guardrail detail sharpening. Static Description: Six-lane divided Autobahn, concrete center barrier, silver metal guardrails, green grass embankments. Overhead green highway signs in the distance. Light ground-level mist. Wet dark asphalt reflecting every light source."},{"lang":"zh","prompt":"风格与氛围：蓝色时刻黄昏，低饱和青钢色调搭配选择性暖橙（#E67E22）尾灯光。变形镜头，浅景深，24帧胶片颗粒感。湿润沥青反光，柔和大气雾霭。企业纪录片质感。动态描述：高角度航拍无人机向六车道德国高速公路俯冲下降。镜头从陡峭鸟瞰角度逐渐压平，持续接近地面。下方密集混合车流双向行驶——白色侧帘半挂车、冷藏厢式拖车、轿车、SUV。近车道红色尾灯从左向右流动，对向车道白色前灯从右向左行进。公路向右缓弯。下降平滑连续，地面逐渐放大，车道标线变得清晰，护栏细节逐渐锐化。静态描述：六车道分隔高速公路，混凝土中央隔离带，银色金属护栏，绿色草坡路堤。远处绿色高架路牌。低层薄雾。深色湿润沥青映射所有光源。"}]
```

---

## Shot 1.2 — Seitlich mitfahrend, GPS + Temperatur Hologramme

> First Frame: Still 1.2

```json
[{"lang":"en","prompt":"Style & Mood: Blue hour dusk, teal shadows with selective orange (#E67E22) accents from HUD panels and tail lights. Anamorphic lens, motion blur on asphalt, 24fps grain. Augmented-reality overlay aesthetic — flat, translucent, integrated into the physical scene. Dynamic Description: Stabilized aerial tracking shot from a 45-degree side angle above and behind the traffic flow. The camera moves with the vehicles at highway speed. Three white curtainside semi-trailers occupy the right lanes at staggered distances — one filling the near foreground, one mid-frame, one further ahead. Small glowing orange rectangular HUD panels hover directly above each trailer roof, translucent and flat. Each panel displays a GPS pin icon with a dotted route line and a thermometer icon beside a horizontal bar gauge. The panels drift with their trailers, edges softly illuminated. Cars and box trucks fill the left lanes, moving slightly faster. Road surface streaks with motion blur. The camera holds its lateral position, steady forward momentum. Static Description: Six-lane German Autobahn at dusk, heavy mixed traffic. Wet asphalt, silver guardrails, green embankments. Light atmospheric haze. Orange HUD panels: flat augmented-reality style, no sci-fi glow — Bloomberg Terminal overlay on physical reality."},{"lang":"zh","prompt":"风格与氛围：蓝色时刻黄昏，青色阴影搭配选择性橙色（#E67E22）HUD面板与尾灯高光。变形镜头，沥青运动模糊，24帧颗粒感。增强现实叠加美学——扁平、半透明、融入物理场景。动态描述：稳定航拍跟拍镜头，从45度侧上方略偏后方跟随车流。摄影机以高速公路速度随车辆移动。三辆白色侧帘半挂车交错占据右侧车道——一辆充满近景前景，一辆居中，一辆更远。小型发光橙色矩形HUD面板悬浮于每辆拖车车顶正上方，半透明且扁平。每个面板显示GPS定位图标配虚线路径，以及温度计图标旁的水平条形仪表。面板随拖车漂移，边缘柔和发光。轿车和厢式货车填满左侧车道，速度略快。路面因运动模糊而拉丝。摄影机保持横向位置，稳定向前推进。静态描述：黄昏六车道德国高速公路，密集混合车流。湿润沥青，银色护栏，绿色路堤。轻微大气雾霭。橙色HUD面板：扁平增强现实风格，非科幻光效。"}]
```

---

## Shot 1.3 — Umflug über Trailer, DCU sendet Daten

> First Frame: Still 1.3

```json
[{"lang":"en","prompt":"Style & Mood: Blue hour dusk, deep teal background with concentrated orange (#E67E22) energy radiating from the DCU. Anamorphic lens, telephoto compression, shallow depth of field isolating the trailer. Technical-reveal aesthetic — controlled, precise, engineered. Dynamic Description: Side-angle aerial shot from the opposite side of a single white curtainside semi-trailer driving left-to-right. The drone hovers at roof height on the oncoming-traffic side, looking across at the trailer's front section. The front wall is fully visible. Mounted on the trailer underside directly behind the front wall, near the kingpin coupling — a small black rectangular electronic unit, the DCU. A subtle orange glow outlines the box, drawing focus. Thin orange concentric radio-wave arcs radiate from the DCU outward and upward, pulsing in rhythmic intervals like a cell-tower signal icon. A faint orange data-stream line extends from the arcs into the darkening sky above. The trailer holds steady speed, background traffic reduced to streaked bokeh. The camera maintains its position alongside, locked on the DCU. Static Description: Single white curtainside trailer on German Autobahn at dusk. DCU: small black rectangular box, underside-mounted behind front wall near kingpin. Wet asphalt, blurred background traffic. Atmospheric haze. Orange signal arcs: concentric, translucent, pulsing upward."},{"lang":"zh","prompt":"风格与氛围：蓝色时刻黄昏，深青色背景中集中的橙色（#E67E22）能量从DCU辐射。变形镜头，长焦压缩，浅景深隔离拖车主体。技术揭示美学——受控、精确、工程化。动态描述：侧角航拍镜头从单辆白色侧帘半挂车对面拍摄，拖车从左向右行驶。无人机悬停于车顶高度的对向车道一侧，横向观察拖车前部。前壁完全可见。安装在拖车底部、紧贴前壁后方靠近主销连接处——一个小型黑色矩形电子单元，即DCU数字控制单元。微妙橙色光晕勾勒盒体轮廓，引导视觉焦点。纤细橙色同心射频波弧从DCU向外向上辐射，以节奏性间隔脉冲跳动，形如基站信号图标。一条淡橙色数据流线从波弧延伸至上方渐暗天空。拖车保持匀速，背景车流化为拉丝散景。摄影机锁定DCU位置，保持侧方跟随。静态描述：黄昏德国高速公路上单辆白色侧帘拖车。DCU：小型黑色矩形盒体，底部安装于前壁后方近主销处。湿润沥青，模糊背景车流。大气雾霭。橙色信号弧：同心、半透明、向上脉冲。"}]
```

---

## Shot 2.1 — Disponent überwacht und steuert die Flotte

> First Frame: Still 2.1

```json
[{"lang":"en","prompt":"Style & Mood: Warm overhead fluorescent office light, monitor glow casting blue-orange on skin. Teal shadows in room corners, selective orange (#E67E22) from the tracking map on center screen. Anamorphic lens, 24fps grain. Operational atmosphere — a room that never sleeps. Dynamic Description: Medium shot from a slight right angle. A fleet dispatcher sits at an L-shaped desk — short gray hair buzzed on the sides, reading glasses pushed onto forehead, dark blue polo shirt with company logo. Three curved widescreen monitors dominate the desk. Center screen: dark European map dense with hundreds of small orange pulsing dots and faint route lines. Left screen: status list rows with colored indicators. Right screen: single trailer route, temperature line graph, ETA countdown. His right hand grips the mouse, clicking — on the center map, a cluster of dots highlights as he selects them. His left hand lifts a wireless headset from the desk toward his ear, jaw setting with purpose. On the desk: a desk phone, half-empty coffee mug, stack of printed route sheets. Behind him on the wall: a large printed European highway map with colored sticky notes marking regions. A glass partition wall on the left shows a larger open-plan office beyond. Static Description: Fleet dispatch office, approximately 5×4 meters. L-shaped desk, three 27-inch widescreen monitors. Desk clutter: phone, mug, route printouts, headset charger. Wall map with sticky notes. Overhead fluorescent panels, warm tone. Glass partition to open office."},{"lang":"zh","prompt":"风格与氛围：温暖顶部荧光灯办公室照明，显示器光芒在皮肤上投射蓝橙色。房间角落青色阴影，选择性橙色（#E67E22）来自中央屏幕追踪地图。变形镜头，24帧颗粒感。运营氛围——一个永不休息的房间。动态描述：中景，略偏右侧角度。一名车队调度员坐在L形桌前——短灰发两侧推剪，老花镜推至前额，深蓝色公司标志Polo衫。三台弧形宽屏显示器占据桌面。中央屏幕：深色欧洲地图密布数百个橙色脉冲小点和淡灰色路线。左屏：状态列表行配彩色指示灯。右屏：单辆拖车路线、温度折线图、预计到达倒计时。右手握住鼠标点击——中央地图上一组点在选中时高亮。左手从桌面拿起无线耳麦举向耳边，下颌因专注而收紧。桌上：座机电话、半空咖啡杯、打印路线单据叠放。身后墙上：大幅印刷欧洲公路地图，彩色便签标注各区域。左侧玻璃隔断墙外可见更大的开放式办公区。静态描述：车队调度室，约5×4米。L形桌，三台27英寸宽屏显示器。桌面物品：电话、咖啡杯、路线打印件、耳麦充电座。墙面地图配便签。顶部荧光灯板，暖色调。通向开放办公区的玻璃隔断。"}]
```

---

## Shot 2.2 — Datacenter / Sicherheit

> First Frame: Still 2.2

```json
[{"lang":"en","prompt":"Style & Mood: Cool-white fluorescent sterility, precise symmetry. Blue and orange (#E67E22) LED pinpoints in darkness between racks. Anamorphic lens, extreme depth vanishing point. Clinical, restricted, zero-tolerance atmosphere. Dynamic Description: Stabilized dolly pushing slowly through a heavy glass security door. A badge reader on the right wall passes out of frame as the camera crosses the threshold. The door frame slides past at the edges. Ahead: two parallel rows of black server racks stretch deep into the room, approximately ten per row, forming a narrow aisle. Blue and orange LED status indicators line each rack in perfect vertical columns, pinpoints of light in the dim inter-rack space. White raised flooring with perforated ventilation tiles reflects the overhead cool-white fluorescents. On the right wall near the entrance, a wall-mounted 24-inch monitor displays a dark security dashboard — green checkmark icons, lock symbols, status bars. Cable management trays run along the ceiling in straight lines. The camera advances slowly, the vanishing point pulling the eye deep into the corridor of racks. The air feels cold and controlled. Static Description: Tier-3 data center server room, approximately 15 meters deep. Heavy glass security door with badge reader. Two rows of black server racks, hot-aisle/cold-aisle. Blue and orange LEDs. White raised flooring, perforated tiles. Cool-white overhead fluorescents. Security dashboard monitor. Ceiling cable trays. Spotless, sterile, organized."},{"lang":"zh","prompt":"风格与氛围：冷白荧光灯无菌感，精确对称构图。机架间隙中蓝色与橙色（#E67E22）LED针点光源。变形镜头，极深消失点透视。临床级、限制进入、零容忍氛围。动态描述：稳定推轨缓慢穿越厚重玻璃安全门。右墙门禁读卡器滑出画面边缘，摄影机越过门槛。门框从画面两侧掠过。前方：两排平行黑色服务器机架向纵深延伸，每排约十台，形成窄通道。蓝色与橙色LED状态指示灯沿每台机架排列成完美垂直列，在机架间暗空间中形成针点光源。白色架高地板配穿孔通风瓷砖映射头顶冷白荧光灯。右墙入口附近，壁挂24英寸显示器显示深色安全仪表盘——绿色勾选图标、锁定符号、状态条。线缆管理桥架沿天花板直线延伸。摄影机缓慢推进，消失点将视线引向机架走廊深处。空气感觉冰冷受控。静态描述：三级数据中心机房，纵深约15米。厚重玻璃安全门配门禁读卡器。两排黑色服务器机架，热通道/冷通道配置。蓝橙LED。白色架高地板，穿孔瓷砖。冷白顶部荧光灯。安全仪表盘显示器。天花板线缆桥架。一尘不染，无菌，井然有序。"}]
```

---

## Shot 2.3 — Engineering-Team + TISAX

> First Frame: Still 2.3

```json
[{"lang":"en","prompt":"Style & Mood: Warm natural daylight flooding through floor-to-ceiling windows, golden hour quality. Teal accent shadows in corners, orange (#E67E22) from whiteboard markers and the TISAX certificate seal. Anamorphic lens, shallow depth of field on the team, background monitors soft. Collaborative, productive, German engineering precision. Dynamic Description: Medium shot from a slight right angle in a bright open-plan office. Three engineers stand around a large wall-mounted whiteboard covered with architecture diagrams in orange and blue markers — boxes connected by arrows, cloud icons, database cylinders. On the left: a figure with shoulder-length dark auburn hair in a low ponytail, charcoal gray blazer over white t-shirt, silver stud earrings — right hand extended, pointing an orange marker at a diagram node, wrist turning slightly as the tip touches the board. Center: a figure with short curly dark blond hair, light stubble, dark olive green henley with sleeves pushed to elbows, arms loosely crossed at chest height, weight shifted to the left foot. Right: a figure with short straight black hair, clean-shaven, dark blue t-shirt, one hand resting on the back of a desk chair, chin dipping in a slight nod. On the wall beside the whiteboard, a framed certificate in a dark frame with an orange seal — the TISAX certification. Standing desks with dual monitors showing abstract dark dashboards fill the background. Green potted plants line the window sills. The camera holds with subtle handheld sway. Static Description: Open-plan German tech office, approximately 60 sqm visible. Floor-to-ceiling south-facing windows, light oak hardwood floor. Wall-mounted whiteboard, 2m wide, architecture diagrams in orange and blue. Framed TISAX certificate with orange seal. Standing desks, dual monitors, dark dashboards. Potted plants on sills. Glass-walled meeting room in far background."},{"lang":"zh","prompt":"风格与氛围：温暖自然日光透过落地窗倾泻，黄金时段质感。角落青色辅助阴影，橙色（#E67E22）来自白板标记笔和TISAX证书印章。变形镜头，团队主体浅景深，背景显示器柔化。协作、高效、德国工程精确性。动态描述：中景，略偏右侧角度，明亮开放式办公室。三名工程师围绕大型壁挂白板，白板上覆盖橙色和蓝色标记笔绘制的架构图——方框由箭头连接，云图标，数据库圆柱体。左侧：一个身影，深赤褐色及肩发束低马尾，炭灰色西装外套内搭白色T恤，银色耳钉——右手伸出，橙色标记笔指向图表节点，手腕微转笔尖触及白板。中间：一个身影，短卷深金发，轻微胡茬，深橄榄绿亨利衫袖口推至肘部，双臂松散交叉于胸前，重心偏左脚。右侧：一个身影，短直黑发，面部干净，深蓝T恤，一只手搭在椅背上，下巴微点表示认同。白板旁墙上，深色画框裱装证书配橙色印章——TISAX认证。站立式办公桌配双显示器显示抽象深色仪表盘填充背景。绿色盆栽植物排列窗台。摄影机保持轻微手持晃动。静态描述：德国科技公司开放式办公室，可见面积约60平方米。朝南落地窗，浅橡木硬木地板。壁挂白板宽2米，橙蓝架构图。裱框TISAX证书配橙色印章。站立桌，双显示器，深色仪表盘。窗台盆栽。远处玻璃隔断会议室。"}]
```

---

---

## Shot 3.1 — Detail: CHAR-B zeichnet am Whiteboard

> First Frame: Still 3.1

```json
[{"lang":"en","prompt":"Style & Mood: Warm natural daylight, golden-hour softness. Shallow depth of field isolating hand and whiteboard. Orange (#E67E22) marker ink as dominant color accent against white board surface. Anamorphic lens bokeh in background. Intimate, precise, hands-on craftsmanship. Dynamic Description: Static close-up locked on a whiteboard surface in a bright office. Architecture diagrams fill the board — rounded rectangular boxes connected by arrows in orange and blue marker, small cloud icons, database cylinder symbols. A right hand enters frame from the lower left, holding an orange whiteboard marker. Short natural nails, a small silver bracelet at the wrist, charcoal gray blazer sleeve visible. The marker tip touches the board and draws a slow connecting arrow between two nodes — the ink line extending smoothly across the white surface. The hand pauses at the endpoint, then lifts the marker. Behind the whiteboard, the background dissolves into warm bokeh: floor-to-ceiling windows, daylight, green potted plant shapes on the sill. Static Description: Bright engineering office. Wall-mounted whiteboard with orange and blue architecture diagrams — boxes, arrows, cloud icons, database cylinders. No readable text. Floor-to-ceiling windows with daylight. Green plants on sills."},{"lang":"zh","prompt":"风格与氛围：温暖自然日光，黄金时段柔和质感。浅景深隔离手部与白板。橙色（#E67E22）标记墨水作为白板表面上主导色彩强调。变形镜头背景散景。亲密、精确、手工匠人感。动态描述：静态特写锁定明亮办公室白板表面。架构图铺满白板——圆角矩形框由橙蓝标记笔箭头连接，小型云图标，数据库圆柱符号。一只右手从画面左下方入画，持橙色白板笔。短自然指甲，腕部小型银色手链，炭灰色西装外套袖口可见。笔尖触及白板，缓慢绘制两个节点间连接箭头——墨线在白色表面平滑延伸。手在终点停顿，随后提起标记笔。白板后方背景化为温暖散景：落地窗、日光、窗台绿色盆栽轮廓。静态描述：明亮工程办公室。壁挂白板配橙蓝架构图——方框、箭头、云图标、数据库圆柱。无可读文字。落地窗配日光。窗台绿植。"}]
```

---

## Shot 3.2 — Disponent und Lead-Architektin im Gespräch

> First Frame: Still 3.2

```json
[{"lang":"en","prompt":"Style & Mood: Warm afternoon daylight from behind, rim-lighting two figures in profile. Teal shadow tones with selective orange (#E67E22) from the tablet screen route map. Anamorphic lens, shallow depth of field. Collaborative moment — operations meets engineering. Dynamic Description: Medium shot in a bright engineering office beside floor-to-ceiling windows. Two figures stand in profile to camera near a standing desk. On the left: a figure with short gray hair buzzed on sides, reading glasses on nose, dark blue polo shirt with company logo — holds a tablet in both hands, screen angled toward the other person. The dark tablet screen shows an orange route map with dot clusters. On the right: a figure with shoulder-length dark auburn hair in a low ponytail, charcoal gray blazer over white t-shirt, silver stud earrings — leans forward, one hand raised, index finger pointing at a spot on the tablet screen. Both faces turned toward the tablet between them, profiles lit by warm window light from behind creating soft rim glow on shoulders and hair edges. In the background: the whiteboard with orange and blue architecture diagrams, and beside it a framed TISAX certificate with dark frame and orange seal. Camera holds with subtle handheld sway. Light oak flooring. Static Description: Bright open-plan engineering office, floor-to-ceiling south-facing windows, afternoon daylight. Standing desk with dual monitors. Whiteboard with architecture diagrams. Framed TISAX certificate. Light oak hardwood floor. Green potted plants on sills."},{"lang":"zh","prompt":"风格与氛围：温暖午后日光从身后照射，轮廓光勾勒两个侧面人影。青色阴影色调搭配选择性橙色（#E67E22）来自平板屏幕路线图。变形镜头，浅景深。协作时刻——运营遇见工程。动态描述：中景，明亮工程办公室，落地窗旁。两个身影侧面朝向摄影机站在站立桌旁。左侧：短灰发两侧推剪，鼻梁上架老花镜，深蓝Polo衫配公司标志——双手持平板电脑，屏幕朝向另一人。深色平板屏幕显示橙色路线图和点群。右侧：深赤褐色及肩发束低马尾，炭灰色西装外套内搭白色T恤，银色耳钉——身体前倾，一只手抬起食指指向平板屏幕某处。两人面部转向两人间的平板，侧脸被身后窗户暖光照亮，肩部和发丝边缘形成柔和轮廓光。背景中：白板配橙蓝架构图，旁边深色画框裱装TISAX证书配橙色印章。摄影机保持轻微手持晃动。浅橡木地板。静态描述：明亮开放式工程办公室，朝南落地窗，午后日光。站立桌配双显示器。白板配架构图。裱框TISAX证书。浅橡木硬木地板。窗台绿植。"}]
```

---

## Shot 3.3 — Visitenkarte / CTA

> First Frame: Still 3.3

```json
[{"lang":"en","prompt":"Style & Mood: Warm daylight, extreme shallow depth of field. Orange (#E67E22) accent bar on the business card as sole color pop against neutral oak and white. Anamorphic lens, macro-like intimacy. Premium, minimal, invitation. Dynamic Description: Extreme close-up in a bright office. A hand in a dark blue polo shirt sleeve descends into frame from above and places a white business card onto a clean light oak desk surface. The card: minimalist design, orange accent bar running vertically along the left edge, dark charcoal text, the URL neogeo.com. The card is crisp white against warm oak wood grain. One index finger holds the top edge for a moment, then lifts away. The camera slowly racks focus — the card blurs as the background sharpens: floor-to-ceiling windows with bright afternoon daylight, the soft silhouettes of the engineering team still gathered at the whiteboard further back in the room. The final frame holds on the warm, bright, blurred window light. Static Description: Engineering office, light oak desk surface with visible wood grain. White business card with orange accent bar. Floor-to-ceiling windows with afternoon daylight. Faint team silhouettes at whiteboard in deep background."},{"lang":"zh","prompt":"风格与氛围：温暖日光，极浅景深。名片上橙色（#E67E22）强调条作为中性橡木和白色中唯一色彩亮点。变形镜头，微距般亲密感。高端、极简、邀请。动态描述：极特写，明亮办公室。一只穿深蓝Polo衫袖口的手从画面上方降入，将白色名片放置于浅橡木桌面。名片：极简设计，左侧边缘垂直橙色强调条，深炭灰色文字，网址neogeo.com。白色名片在温暖橡木纹理上清晰锐利。食指按住上缘片刻，随后抬起。摄影机缓慢转换焦点——名片模糊，背景锐化：落地窗明亮午后日光，工程团队仍聚集在远处白板旁的柔和剪影。最终画面停留在温暖、明亮、虚化的窗户光线上。静态描述：工程办公室，浅橡木桌面可见木纹。白色名片配橙色强调条。落地窗配午后日光。深景中白板旁团队淡影。"}]
```

---

## Text-Overlays (Post-Production)

**Szene 1:**
- Shot 1.1: *"Was passiert, wenn jeder Trailer ein IoT-Gerät wird?"*
- Shot 1.2: *"GPS. Temperatur. Reifendruck. Alles in Echtzeit."*
- Shot 1.3: *"Von der Straße direkt in die Cloud."*

**Szene 2:**
- Shot 2.1: *"Zehntausende Trailer. 20+ Länder. Eine Plattform."*
- Shot 2.2: *"TISAX Stufe 3 — höchste Sicherheitsstufe"*
- Shot 2.3: *"Architektur. Code. Betrieb. Alles aus einer Hand."*

**Szene 3:**
- Shot 3.1: *"30+ Jahre Engineering. Deutsches Team."*
- Shot 3.2: *"Alleiniger Entwicklungspartner. 100% Eigenleistung."*
- Shot 3.3: *"Bereit für Ihre IoT-Plattform? → neogeo.com"*
