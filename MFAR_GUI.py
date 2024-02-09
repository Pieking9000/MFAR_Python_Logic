import PySimpleGUI as gui
import MFAR_Logic as logic

def main():
    titleText = "Metroid Fusion Alternative Randomizer"
    randoSettings = [
        [
            gui.Text("Difficulty"),
            gui.Slider(range=(0, 5), orientation="h", key="diffSlider")
            ],
        [gui.Checkbox(text="Major/Minor Item Split", key="majMin")],
        [gui.Checkbox(text="Missile Upgrades Enable Missiles", key="missUp")],
        [gui.Checkbox(text="Use Power Bombs Without Bombs", key="usePB")],
        [gui.Checkbox(text="Logical Damage Runs", key="damageRuns")],
        [gui.Checkbox(text="Split Security Levels", key="splitSec")],
        [gui.Checkbox(text="Sector Shuffle", key="sectorShuffle")],
        [gui.Checkbox(text="Show Community Names", key="showCommNames")]
        
        ]
    layout = [
        [gui.Text(titleText)],
        [randoSettings],
        [gui.Button("Exit")]
        ]
    window = gui.Window("MFAR", layout)

    while True:
        event, values = window.read()
        if event == "Exit" or event == gui.WIN_CLOSED:
            break
    window.close()
    logic.initRando(bool(values.get("majMin")), bool(values.get("missUp")), bool(values.get("usePB")), bool(values.get("damageRuns")), bool(values.get("splitSec")), bool(values.get("sectorShuffle")), bool(values.get("showCommNames")), int(values.get("diffSlider")))
    

if __name__ == "__main__":
    main()
