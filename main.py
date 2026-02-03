import cv2
import mediapipe as mp
import numpy as np
import pyvista as pv
import time
from collections import deque
from scipy.spatial import cKDTree

# ==========================================================
# PYVISTA FIX
# ==========================================================
pv.global_theme.allow_empty_mesh = True

# ==========================================================
# AYARLAR
# ==========================================================
CAM_INDEX = 0
SMOOTH_ALPHA = 0.85
DEPTH_SCALE = 3.0
RENDER_LIMIT = 300
FONT = cv2.FONT_HERSHEY_SIMPLEX

# ==========================================================
# MEDIAPIPE
# ==========================================================
mp_face = mp.solutions.face_mesh
face_mesh = mp_face.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
)

# ==========================================================
# KAMERA
# ==========================================================
cap = cv2.VideoCapture(CAM_INDEX)
if not cap.isOpened():
    raise RuntimeError("Kamera açılamadı")

# ==========================================================
# VERİ
# ==========================================================
ema_pos = None
positions_all = []
positions_render = []
fps_q = deque(maxlen=30)

# ==========================================================
# PYVISTA – ANA SAHNE
# ==========================================================
plotter = pv.Plotter(window_size=(1000, 700))
plotter.set_background("#0b0b0b")
plotter.add_title("Face Tracking", font_size=16)
plotter.show_grid(color="gray")

# ODA
room = pv.Box(bounds=(-1.2, 1.2, -1.0, 1.0, -4.0, 0.0))
plotter.add_mesh(room, style="wireframe", opacity=0.25)

# ARKA DUVAR
back_wall = pv.Plane(
    center=(0, 0, 0),
    direction=(0, 0, 1),
    i_size=2.4,
    j_size=2.0
)
plotter.add_mesh(back_wall, color="#1f1f1f", opacity=0.4)

# KAFAN
head_actor = plotter.add_mesh(pv.Sphere(radius=0.06), color="lime")

# TRAIL
trail_poly = pv.PolyData(np.empty((0, 3)))
plotter.add_mesh(trail_poly, color="cyan", line_width=2, opacity=0.6)

# KAMERA
plotter.camera.position = (0, 0, 0.2)
plotter.camera.focal_point = (0, 0, -2)
plotter.camera.up = (0, 1, 0)

plotter.show(auto_close=False, interactive_update=True)

print("🎥 Çalışıyor | ESC → Çıkış & RAPOR")

# ==========================================================
# ANA DÖNGÜ
# ==========================================================
while True:
    t0 = time.time()
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    res = face_mesh.process(rgb)

    if res.multi_face_landmarks:
        lm = res.multi_face_landmarks[0].landmark
        nose = lm[1]
        left = lm[234]
        right = lm[454]

        cx = (nose.x - 0.5) * 2
        cy = -(nose.y - 0.5) * 2
        face_w = np.linalg.norm([left.x - right.x, left.y - right.y])
        z = -face_w * DEPTH_SCALE

        pos = np.array([cx, cy, z])
        ema_pos = pos if ema_pos is None else SMOOTH_ALPHA * ema_pos + (1 - SMOOTH_ALPHA) * pos

        positions_all.append(ema_pos.copy())
        positions_render.append(ema_pos.copy())

        if len(positions_render) > RENDER_LIMIT:
            positions_render.pop(0)

        head_actor.SetPosition(*ema_pos)

        if len(positions_render) > 1:
            pts = np.array(positions_render)
            lines = pv.lines_from_points(pts)
            trail_poly.points = lines.points
            trail_poly.lines = lines.lines

        plotter.render()

    fps_q.append(1 / max(1e-6, time.time() - t0))
    cv2.putText(frame, f"FPS: {sum(fps_q)/len(fps_q):.1f}", (20, 40),
                FONT, 0.8, (255, 255, 255), 2)
    cv2.imshow("Face Tracking By Volkan", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

# ==========================================================
# TEMİZLEME
# ==========================================================
cap.release()
cv2.destroyAllWindows()
plotter.close()

# ==========================================================
# 🔥 HEAT MAP RAPORU
# ==========================================================
pts = np.array(positions_all)

if len(pts) > 50:
    tree = cKDTree(pts)
    density = np.array([len(tree.query_ball_point(p, r=0.15)) for p in pts])

    cloud = pv.PolyData(pts)
    cloud["density"] = density

    report = pv.Plotter(window_size=(900, 650))
    report.set_background("#111111")
    report.add_title("Heat Map", font_size=20)

    # ODA REFERANSI (ÇOK ÖNEMLİ)
    report.add_mesh(room, style="wireframe", opacity=0.15)
    report.add_mesh(back_wall, color="#222222", opacity=0.3)

    report.add_mesh(
        cloud,
        scalars="density",
        render_points_as_spheres=True,
        point_size=8,
        cmap="inferno",
        scalar_bar_args={"title": "Visited Density"}
    )

    report.camera.position = (0, 0.6, 1.5)
    report.camera.focal_point = (0, 0, -2)
    report.camera.up = (0, 1, 0)

    report.show()
