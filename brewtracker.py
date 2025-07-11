import tkinter as tk
from tkinter import ttk, messagebox, filedialog

class BeerJournalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Beer Brewing Journal")

        # Set up a scrollable frame
        canvas = tk.Canvas(root)
        scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.entries = {}
        self.build_form()

    def add_field(self, label, field_name, width=50, height=1, row=0, column=0):
        """Adds a field to the grid layout."""
        ttk.Label(self.scrollable_frame, text=label).grid(row=row, column=column, sticky="w", padx=10, pady=(10, 0))
        if height > 1:
            text = tk.Text(self.scrollable_frame, width=width, height=height)
            text.grid(row=row, column=column + 1, padx=10, pady=5, sticky="w")
            self.entries[field_name] = text
        else:
            entry = ttk.Entry(self.scrollable_frame, width=width)
            entry.grid(row=row, column=column + 1, padx=10, pady=5, sticky="w")
            self.entries[field_name] = entry

    def build_form(self):
        """Builds the form with sections and fields in a grid layout."""
        sections = [
            ("General Info", [
                ("Brew Name", "brew_name"),
                ("Style", "style"),
                ("Batch # / Code", "batch_code"),
                ("Date Brewed", "date_brewed"),
                ("Brewer(s)", "brewer"),
                ("Target ABV / OG / FG", "target_stats"),
            ]),
            ("Recipe Details", [
                ("Batch Size", "batch_size"),
                ("Boil Time (min)", "boil_time"),
                ("Estimated IBU", "ibu"),
                ("Grain Bill (list)", "grain_bill", 5),
                ("Hop Schedule (list)", "hop_schedule", 5),
                ("Yeast Strain", "yeast_strain"),
                ("Form (Liquid/Dry)", "yeast_form"),
                ("Starter Used", "yeast_starter"),
                ("Fermentation Temp Target", "ferment_temp"),
                ("Additives (list)", "additives", 3),
            ]),
            ("Brewing Process", [
                ("Strike Water Temp", "strike_temp"),
                ("Mash Temp & Duration", "mash_details"),
                ("Boil Start Time", "boil_start"),
                ("Boil End Time", "boil_end"),
                ("Post-Boil Volume", "post_boil_volume"),
                ("Cooling Method", "cooling_method"),
                ("Time to Cool", "cooling_time"),
                ("Temperature at Pitching", "pitch_temp"),
            ]),
            ("Fermentation", [
                ("Primary Vessel", "vessel"),
                ("Date Yeast Pitched", "yeast_pitch_date"),
                ("Fermentation Temp Range", "ferment_range"),
                ("Active Fermentation Duration", "ferment_duration"),
                ("Transferred to Secondary? (Y/N + Date)", "secondary_transfer"),
                ("Dry Hopped? (Y/N + details)", "dry_hop"),
            ]),
            ("Measurements", [
                ("Original Gravity (OG)", "og"),
                ("Final Gravity (FG)", "fg"),
                ("Calculated ABV", "abv"),

            ]),
            ("Bottling / Kegging", [
                ("Date Bottled / Kegged", "bottle_date"),
                ("Priming Sugar Used", "priming_sugar"),
                ("Packaging Type & Quantity", "packaging"),
            ]),
            ("Tasting Notes", [
                ("Date First Sampled", "sample_date"),
                ("Clarity", "clarity"),
                ("Head Retention", "head_retention"),
                ("Aroma", "aroma", 2),
                ("Flavor", "flavor", 2),
                ("Mouthfeel", "mouthfeel", 2),
                ("Balance", "balance"),
                ("Off-Flavors", "off_flavors"),
                ("Improvements / Next Time", "improvements", 2),
            ]),
            ("Final Thoughts", [
                ("Success Scale (1-10)", "rating"),
                ("What Went Well", "what_went_well", 2),
                ("What to Change", "what_to_change", 2),
                ("Would Brew Again? (Y/N)", "brew_again"),
                ("Misc Notes", "misc", 2),
            ])
        ]

        row = 0
        for section, fields in sections:
            # Add section header
            ttk.Label(self.scrollable_frame, text=f"== {section} ==", font=("Courier", 12, "bold")).grid(
                row=row, column=0, columnspan=2, sticky="w", pady=(15, 5)
            )
            row += 1
            for field in fields:
                if len(field) == 3:
                    self.add_field(field[0], field[1], height=field[2], row=row, column=0)
                else:
                    self.add_field(field[0], field[1], row=row, column=0)
                row += 1

        # Add Save button
        ttk.Button(self.scrollable_frame, text="Save Journal Entry", command=self.save_entry).grid(
            row=row, column=0, columnspan=2, pady=20
        )

    def save_entry(self):
        content = ""
        for key, widget in self.entries.items():
            if isinstance(widget, tk.Text):
                value = widget.get("1.0", "end").strip()
            else:
                value = widget.get().strip()
            content += f"{key.replace('_', ' ').title()}:\n{value}\n\n"

        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt")],
            title="Save Brew Journal Entry"
        )

        if file_path:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(content)
            messagebox.showinfo("Saved", f"Brew journal saved to:\n{file_path}")


if __name__ == "__main__":
    root = tk.Tk()
    app = BeerJournalApp(root)
    root.mainloop()
