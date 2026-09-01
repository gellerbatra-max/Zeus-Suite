# Function Definitions — ## IGES Translator (Import/Export)
*A command-line (typed-command) utility for moving pattern piece data between AccuMark and other CAD systems, using the IGES file format that many design and engineering programs understand.*

### Export — IGESOUT.EXE (send an AccuMark piece OUT to another CAD system)
**Command: `IGESOUT [options] <storage_area> <piece_name> <IGES_filename>`** — This is the command you type to take one pattern piece that's already stored in AccuMark and save a copy of it as an IGES file, which other CAD/drafting software can then open. You tell it which storage area (folder) the piece is in, the piece's name, and what to name the new file.

**`/?` or `/h`** — Displays a quick help screen showing how to use the command, in case you forget the exact typing.

**`/U<u>`** — Lets you force the exported file to use a specific measurement unit instead of whatever unit the piece's storage area normally uses. Type `/U1` for inches, `/U2` for millimeters, or `/U10` for centimeters, depending on what the receiving system expects.

### Import/Convert — IGES.EXE (bring a piece IN from another CAD system)
**Command: `IGES <input-specification> <output-specification> [options]`** — This is the command that reads an IGES file (created by some other CAD system) and converts it into a format AccuMark can use. You give it the incoming file name and either a new file name to save the converted data to, or (if using the `/o` option below) the AccuMark storage area to save it into directly.

**`-A<n>`** — "Closure Amount." Real-world drawings sometimes have tiny gaps where lines that should meet don't quite touch. This option tells the converter how big a gap (in hundredths of an inch) it's allowed to close automatically so the piece's outline forms a proper closed shape instead of failing to convert.

**`-T<d>`** — "Trimming." Removes unnecessary extra points that fall on a perfectly straight line, which keeps the piece file smaller and can make the software run faster. The optional number controls how pickly it decides a point is "unnecessary."

**`-G`** — "Grade Points." Marks certain points on the piece as grade points (points used when scaling the piece up or down for different sizes), based on numbering already present in the incoming file.

**`-MA<n>`** — Limits how many points are used to draw a curved arc, which prevents very large, highly-curved shapes from overwhelming the system.

**`-MB<n>`** — Same idea as above, but for smooth curved lines called "splines" instead of simple arcs.

**`-I`** — "Pasting Internals." If an internal marking (like a pocket line) inside the piece has its ends touching the piece's outer edge, this option automatically converts it into a notch (a small cutting guide mark) instead of leaving it as a separate internal line.

**`-L`** — Shows a running list of what the program is doing on screen as it works. This is mainly useful for troubleshooting if a conversion isn't working right.

**`-P`** — Same as above, but sends that troubleshooting information to a printer instead of the screen.

**`-D`** — Converts single-point markings from the incoming file (like small drilled reference holes) into AccuMark's "drill hole" markings.

**`-U<u>`** — Corrects the piece's measurement unit if the incoming file was created using a different unit than expected (for example, forcing centimeters with `-U10` if the piece is coming out oddly sized due to a units mismatch).

**`-S`** — Forces every point on the piece to be treated as a sharp corner rather than a smooth curve. Used when the piece is coming in with unwanted curve-smoothing applied.

**`-O<storage_area>`** — "Online to AccuMark." Instead of just saving a converted file to disk, this option sends the converted piece straight into a named AccuMark storage area, skipping the separate manual import step described below.

### IGES.INI — a one-time setup file that saves retyping the same options every time
**`StorageAreaName=`** — Pre-sets which AccuMark storage area conversions should go into, so you don't have to type the `-O` option every single time you run a conversion.

**`PieceNameAtLine=`** — Tells the converter which line of the incoming file already contains the piece's name, so it can read the name automatically instead of you having to type it in.

**`DescriptionAtLine=`** — Same idea, but for automatically reading the piece's description text from the incoming file.

**`CategoryAtLine=`** — Same idea, but for automatically reading the piece's category (type of piece) from the incoming file.

### After converting (if not sent directly into AccuMark)
**Run AccuMark's IMPORT DATA editor** — If the converted piece was saved to a file rather than sent directly into AccuMark storage (see `-O` above), you open this editor in AccuMark, choose "DIGITIZE DATA" as the type of data, and tell it where the converted file is and which storage area to put it in.

**Press F1 or select PROCESS** — This is the button/key that actually runs the import after you've filled in the editor, pulling the converted piece into the AccuMark database.

**Verify the piece** — After importing, open the piece in Pattern Design and visually check that its outline, notches, and internal markings all came through correctly before using it in production.
