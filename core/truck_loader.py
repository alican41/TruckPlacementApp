import pandas as pd
from typing import List, Set
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from math import ceil

class Box:
    def __init__(self, box_no: str, box_type: str, weight: float):
        self.box_no = box_no
        self.box_type = self._standardize_box_type(box_type)
        self.weight = weight
        self.height = self._get_height(self.box_type)

    def _standardize_box_type(self, box_type: str) -> str:
        if isinstance(box_type, str):
            box_type = box_type.strip().upper()
            if "BÜYÜK" in box_type:
                return "BUYUK"
            elif "ORTA" in box_type:
                return "ORTA"
            elif "KÜÇÜK" in box_type:
                return "KUCUK"
            elif "PALET" in box_type:
                return "PALET"
            elif "KATLI RAF" in box_type:
                return "PROJECT"
            elif "BATTAL BOY" in box_type:
                return "BATTAL"
        return box_type

    def _get_height(self, box_type: str) -> int:
        heights = {
            "BUYUK": 3,
            "ORTA": 2,
            "KUCUK": 1,
            "PALET": 3,
            "PROJECT": 6,
            "BATTAL": 7
        }
        return heights.get(box_type, 0)

    def __str__(self):
        return f"{self.box_no} ({self.box_type}): {self.weight:.1f}kg, Y:{self.height}x"


class TruckArea:
    def __init__(self, area_no: int):
        self.area_no = area_no
        self.boxes: List[Box] = []
        self.total_weight = 0
        self.total_height = 0
        self.max_height = 6
        self.has_palet = False

    def can_add_box(self, box: Box) -> bool:
        if box.box_type == "PALET" and self.has_palet:
            return False
        return self.total_height + box.height <= self.max_height

    def add_box(self, box: Box) -> bool:
        if self.can_add_box(box):
            self.boxes.append(box)
            self.total_weight += box.weight
            self.total_height += box.height
            if box.box_type == "PALET":
                self.has_palet = True
            return True
        return False

    def clear(self):
        self.boxes.clear()
        self.total_weight = 0
        self.total_height = 0
        self.has_palet = False

    def __str__(self):
        return f"Alan {self.area_no}: " + " + ".join(str(box) for box in self.boxes) + \
            f" | Toplam: {self.total_weight:.1f}kg, Y:{self.total_height}x"


class TruckLoader:
    def __init__(self):
        self.areas: List[TruckArea] = [TruckArea(i + 1) for i in range(32)]
        self.MAX_FIRST_SECTION_WEIGHT = 5000
        self.MAX_TRUCK_WEIGHT = 24000
        self.ilk10Alan = 0
        self.toplamAlan = 0

    def load_excel_data(self, excel_path: str) -> List[Box]:
        df = pd.read_excel(excel_path)
        boxes = []
        for _, row in df.iterrows():
            box_no = str(row['BOX NO'])
            box_type = str(row['BOYUT']) if pd.notna(row['BOYUT']) else None
            weight = float(row['DOLU KG'])

            if box_type:
                boxes.append(Box(box_no, box_type, weight))

        return boxes

    def optimize_first_section(self, boxes: List[Box], used_boxes: Set[str]) -> bool:
        boxes_sorted = sorted(boxes, key=lambda x: (-x.height, x.weight))
        target_height = min(6, sum(box.height for box in boxes_sorted if box.box_no not in used_boxes) // 10)
        if target_height < 1:
            target_height = 1

        for _ in range(300):
            for area in self.areas[:10]:
                area.clear()

            total_weight = 0
            area_boxes = {i: [] for i in range(10)}

            for i in range(10):
                available_boxes = [box for box in boxes_sorted if box.box_no not in used_boxes and
                                   box.box_no not in [b.box_no for j in range(10) for b in area_boxes[j]]]

                placed_box = False
                for box in available_boxes:
                    if (box.height <= self.areas[i].max_height and
                            total_weight + box.weight <= self.MAX_FIRST_SECTION_WEIGHT):
                        area_boxes[i].append(box)
                        total_weight += box.weight
                        available_boxes.remove(box)
                        placed_box = True
                        break

                if not placed_box:
                    break

            if any(len(area_boxes[i]) == 0 for i in range(10)):
                continue

            for i in range(10):
                current_height = sum(box.height for box in area_boxes[i])
                available_boxes = [box for box in boxes_sorted if box.box_no not in used_boxes and
                                   box.box_no not in [b.box_no for j in range(10) for b in area_boxes[j]]]

                while available_boxes and current_height < target_height:
                    best_box = None
                    best_diff = float('inf')

                    for box in available_boxes:
                        if current_height + box.height <= self.areas[i].max_height:
                            if box.box_type == "PALET" and any(b.box_type == "PALET" for b in area_boxes[i]):
                                continue

                            diff = abs((current_height + box.height) - target_height)
                            potential_weight = total_weight + box.weight
                            if potential_weight <= self.MAX_FIRST_SECTION_WEIGHT and (diff < best_diff or
                                                                                      (diff == best_diff and box.weight < best_box.weight if best_box else True)):
                                best_box = box
                                best_diff = diff

                    if best_box:
                        area_boxes[i].append(best_box)
                        current_height += best_box.height
                        total_weight += best_box.weight
                        available_boxes.remove(best_box)
                    else:
                        break

            for i in range(10):
                for box in [b for b in boxes_sorted if b.box_no not in used_boxes and
                                                       b.box_no not in [bx.box_no for j in range(10) for bx in area_boxes[j]]]:
                    current_height = sum(b.height for b in area_boxes[i])
                    if (current_height + box.height <= self.areas[i].max_height and
                            total_weight + box.weight <= self.MAX_FIRST_SECTION_WEIGHT):
                        if box.box_type == "PALET" and any(b.box_type == "PALET" for b in area_boxes[i]):
                            continue
                        area_boxes[i].append(box)
                        total_weight += box.weight

            for i in range(10):
                for box in area_boxes[i]:
                    self.areas[i].add_box(box)

            if (all(len(area.boxes) > 0 for area in self.areas[:10]) and
                    total_weight <= self.MAX_FIRST_SECTION_WEIGHT):
                for i in range(10):
                    for box in area_boxes[i]:
                        used_boxes.add(box.box_no)
                return True

            import random
            random.shuffle(boxes_sorted)

        return False

    def optimize_remaining_sections(self, boxes: List[Box], used_boxes: Set[str]) -> bool:
        available_boxes = [box for box in boxes if box.box_no not in used_boxes]
        total_height = sum(box.height for box in available_boxes)
        target_height_per_area = min(6, total_height / 22)

        for i in range(10, 32):
            self.areas[i].clear()

        available_boxes.sort(key=lambda x: (x.height, -x.weight), reverse=True)

        for box in available_boxes[:]:
            placed = False
            min_height_area_idx = min(range(10, 32),
                                      key=lambda i: self.areas[i].total_height if self.areas[i].can_add_box(box) else float('inf'))

            if min_height_area_idx >= 10 and min_height_area_idx < 32 and self.areas[min_height_area_idx].can_add_box(box):
                if self.areas[min_height_area_idx].add_box(box):
                    used_boxes.add(box.box_no)
                    available_boxes.remove(box)
                    placed = True

            if not placed:
                break

        for box in available_boxes[:]:
            for i in range(10, 32):
                if self.areas[i].can_add_box(box):
                    self.areas[i].add_box(box)
                    used_boxes.add(box.box_no)
                    available_boxes.remove(box)
                    break

        return len(available_boxes) == 0

    def optimize_loading(self, excel_path: str) -> str:
        boxes = self.load_excel_data(excel_path)
        used_boxes = set()

        if not self.optimize_first_section(boxes, used_boxes):
            return "İlk 10 alan için uygun yerleşim bulunamadı!"

        if not self.optimize_remaining_sections(boxes, used_boxes):
            return "Tüm boxlar yerleştirilemedi!"

        result = "TIR YÜKLEMESİ PLANI\n\n"
        result += "İLK 10 ALAN (Maksimum 5000 kg):\n"
        result += "-" * 100 + "\n"
        first_section_weight = sum(area.total_weight for area in self.areas[:10])
        for area in self.areas[:10]:
            result += str(area) + "\n"
        result += f"\nİlk 10 Alan Toplam Ağırlık: {first_section_weight:.1f} kg\n"
        result += "-" * 100 + "\n\n"
        self.ilk10Alan = first_section_weight

        result += "KALAN 22 ALAN:\n"
        result += "-" * 100 + "\n"
        remaining_weight = sum(area.total_weight for area in self.areas[10:])
        for area in self.areas[10:]:
            result += str(area) + "\n"
        result += f"\nKalan Alanlar Toplam Ağırlık: {remaining_weight:.1f} kg\n"
        result += "-" * 100 + "\n\n"

        total_weight = first_section_weight + remaining_weight
        result += f"TIR TOPLAM AĞIRLIK: {total_weight:.1f} kg\n"
        self.toplamAlan = total_weight

        return result

    def plot_truck_layout(self, output_path: str = "truck_layout.pdf"):
        num_areas = len(self.areas)
        half = ceil(num_areas / 2)
        pages = [self.areas[:half], self.areas[half:]]

        with PdfPages(output_path) as pdf:
            for page_num, page_areas in enumerate(pages, start=1):
                fig, ax = plt.subplots(figsize=(11.7, 8.3))
                ax.set_xlim(0, 2)
                ax.set_ylim(0, len(page_areas) // 2 - 1)

                rows = 8
                cols = 2

                for i, area in enumerate(page_areas):
                    col = i % cols
                    row = i // cols
                    x = col * 1
                    y = (rows - row - 1) * 1

                    box_info = "\n".join([f"{box.box_no} ({box.box_type}): {box.weight:.1f} kg" for box in area.boxes])
                    total_weight_info = f"Toplam: {area.total_weight:.1f} kg"
                    full_info = f"Alan {area.area_no}\n{box_info}\n{total_weight_info}"

                    ax.text(x + 0.5, y + 0.5, full_info, ha='center', va='center', fontsize=8,
                            bbox=dict(facecolor='lightgrey', edgecolor='black'))

                ax.set_xticks([])
                ax.set_yticks([])
                ax.set_title(f"TIR DİZİLİMİ - Sayfa {page_num}", fontsize=16)
                plt.tight_layout()
                pdf.savefig(fig)
                plt.close(fig)