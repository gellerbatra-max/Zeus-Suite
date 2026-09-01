# Richpeace GMS (Garment Marking System) — Full Function Catalogue
*312 documented functions, extracted from the Richpeace V8.0 manual*

**A, B, C, D** — An alternative set of parameters used to define the stripe geometry instead of the X/Y/distance/angle method.

**About** — Displays version, VID, copyright, and other system information. Accessed via 【Help】--【About】, showing a dialogue box that is closed by clicking 【OK】 after checking.

**Add** — In the Define Stripe Marks dialog, opens the Add Mark dialog where the user can freely name a new mark; clicking OK returns to the previous dialog, and Add can be clicked repeatedly to create multiple marks.

**Add piece** — Increases or decreases the quantity of a piece, either for a single selected size or for all sizes at once. Select the size, open the tool, enter a quantity with a + or - prefix, optionally select all sizes, then click OK.

**Add pieces** — Adds additional pieces of the same sizes from the currently loaded file or from another pattern file (DGS, PTN, or PDS) into the current marker.

**Adjust Stripe** — A show/hide toggle used to enable adjustment of stripe or grid position for materials with stripes and grids; works together with the Stripe Definition command that sets the intervals between stripes or grids.

**Align** — Aligns two or more selected pieces on the marker according to a chosen alignment mode, such as Left, Right, Top, Bottom, Horizontal Center, or Vertical Center.

**All folded pieces** — Selects every folded pattern piece present on the marker.

**All Markers** — If ticked, saves all markers in the file; if unticked, only the current marker is saved.

**All Size Info** — Sets the size attribute for all sizes of the selected pieces simultaneously, using mostly the same fields as Piece Info; changes apply to all sizes of the selected piece.

**All the notch same height, Width** — When selected, allows setting the same notch height and width for all notches.

**Apply** — Applies the currently selected mark sign to the selected notch or drill on the piece.

**Area** — Displays the area of the selected piece.

**Associate** — Links a marker's aligned pieces to their original DGS pattern file so that if a piece is revised in DGS afterward, the marker updates that piece automatically instead of requiring the piece to be re-aligned; the marker filename cannot be changed when using this function. Parameters let you specify whether the pattern name and material match exactly, whether only the name matches, and whether to use the original or updated (DGS) shrinkage values.

**Attribute** — Defines the piece attribute such as single piece, left piece, right piece, and pairing or folded mode. If a piece's quantity is 2 with pairing enabled, one becomes left and the other right; if pairing is not ticked, both remain identical pieces.

**Auto Nesting - Normal** — When selected, the system places all pieces on the marker according to the priority order set in Nesting > Start Autonesting during automatic marker making.

**Auto Save** — Automatically saves the marker file at a set time interval to its original path and filename, preventing loss of work due to power failure or other issues. Enabled via Option -> Auto Save, ticking Enable Auto Save and entering an interval; if the marker was never saved before, a Save As dialog appears when the interval is reached.

**Auto Set cutting Order** — Recreates the cutting order automatically after it has been manually edited, via Cutter -> Auto Set Cutting Order, so the auto cutter can cut according to the new order.

**Auxiliary line** — Shows the auxiliary line on pieces when ticked, or hides it when unticked.

**Avoide horizontal color shade** — When selected, nests pieces from left to right to avoid horizontal color shading across the marker.

**Avoide vertical color shade** — When selected, nests pieces from top to bottom to avoid vertical color shading across the marker.

**Back up when save** — When manually saving, creates a backup copy in the appointed directory; only the most recent save is kept as backup, replacing the previous backup each time.

**Bind Pattern** — Binds any patterns on the marker together so their relative positions do not change during marker making, forming a single group. Used by selecting the patterns to bind and clicking the bind pattern button.

**Border** — Outputs the marker with a border line when printed or plotted; ticking this option is recommended.

**Both** — Defines whether the piece is symmetric. If the piece count is 2 and symmetry is Yes, the two pieces are mirrored (right and left); if No, the two pieces are identical. A related option, 'Set Both-Attribute if pieces count is even,' can set this automatically.

**Bottom** — Defines the bottom margin of the marker border.

**Bottom fold** — Folds a piece along its bottom side for tubular marker nesting where the piece requires top-bottom symmetry; the piece appears folded in half and stays on the folded side of the marker.

**Browse** — Within the Save Current Solution dialog, lets you save the current marker under a chosen filename, with subsequent saves of similarly named markers getting an added serial number.

**Calculate Efficiency and Marker Length** — Calculates the required material (marker) length based on a target nesting efficiency. The user clicks Calculate -> Calculate Efficiency and Marker Length, inputs the desired efficiency, and the system computes the corresponding material length.

**Calculate material weight** — Calculates the weight of the material used for the marker. After pieces are aligned, the user clicks this command, enters the weight per unit in the dialog box, and the system automatically computes the weight (width x length x plies x weight per unit).

**Cancel encrypt** — Removes encryption from a file that has already been encrypted, by entering the correct password in the dialog box.

**Cap nest** — Defines the nesting method for pieces (e.g., normal, interleaving, reverse). After selecting pieces and opening the tool, a 'Cap pieces nesting' dialog lets you choose the nesting Mode and optionally tick Same distance, Nest whole row only, and Show distance before applying the nest to the particular size.

**Center Rotation** — Rotates a pattern around a clicked center point, similarly constrained by grain line settings (180 degrees for Double-way, 90 degrees for Four-way, free for Any) when selected, or free rotation when not selected. Pressing 1 (clockwise) or 3 (anti-clockwise) rotates by one degree per click, and the exact rotation increment can be set via Option - Set Parameter - Degree.

**Change Distance Between Pattern** — Sets the minimum allowed distance between patterns on the marker via a dialog box.

**Change Width of Marker** — Changes the width of the marker and automatically rearranges the patterns to fit. Opens a dialog to select a module and input the new marker width before confirming.

**Check before plotting or printing** — Lets the user select checks (UnNested Pieces, pieces in aided marker, Fit symmetry, Different Material) that, when triggered, cause the system to prompt a confirmation before plotting or printing.

**Check Current Solution** — Checks the current marker layout solution, showing completed sets, uncompleted sets, and overlapped pieces. It lets the user view original sets, piece quantity per set, and incomplete pieces for a selected pattern and size, and can flash/select complete or incomplete pieces on the marker.

**Check Overlapped Pieces** — Checks the marker for overlapping pieces, highlighting overlaps (shown non-filled) and popping up a warning dialog. It can also report how many overlaps exceed a specified value and show the largest overlap value found.

**Clean aided marker** — Moves all pieces currently on the auxiliary marker back to the piece box.

**Clean marker** — Clears all pieces from the marker and moves them from the working area back into the piece list box, after confirming in a dialog box. Shortcut: Ctrl+C.

**Clear** — Deletes all stripe marks at once.

**Clear aided marker** — When selected, clears the aided marker pattern and makes the marker together with other patterns when using supernest; when not selected, the aided marker is not included when making a marker with supernest.

**Close** — Closes the Define Stripe Marks dialog once all desired marks have been added.

**Close (button)** — Closes the Total Piece Info dialog once all setup for piece/size information has been completed.

**Close HP-GL File** — Closes a previously opened HP-GL file, accessed via File - Close HP-GL after the file has been opened.

**Close Pieces Display Bar** — Opens and closes the Piece Window using a toggle button; when the button is pressed in, the piece window is open, and when it is out, the piece window is closed.

**Code** — Defines the code of the piece, such as a series number or a code representing the piece type.

**Color of set** — When ticked, pieces are shown colored according to their set; when unticked, pieces are shown colored according to their size. Colors for set and size can be changed via the Color command.

**Color Printing** — Prints the marker using color printing.

**Combine notch and border line (All the notch turn to V type)** — When selected, all notches are converted to V-type notches for connection with an auto cutter even if the border line is not V type; otherwise notches are cut in their original type.

**Comment** — Field used to fill in the marker description; when ticked in the comment box under Parameter > Plot or Print, this comment is output when plotting or printing.

**Compact Marker** — Compacts all patterns on the marker toward the left/front direction to improve marker efficiency. Opens a 'compact marker' dialog where a module is selected and confirmed.

**Context help** — Provides a shortcut for accessing help on other tools. Select this tool, then click any other tool to display its Help dialog.

**Correct error** — Used to calibrate/correct the plotted output size after plotting (not the real size itself); requires a password, then you plot a 1m x 1m test rectangle, measure its actual width and length, and input those measured values to correct future plot scaling.

**Current Plotter** — A dropdown in the Plotter dialog used to select which plotter model to use for output.

**Current size only** — When ticked, edits made in Total Piece Info apply only to the currently selected size of the selected piece rather than to all sizes, after clicking Apply.

**Custom Toolbar** — Allows the user to create a custom toolbar by selecting a toolbar category, choosing icons to add, reordering them with Up/Down buttons, and confirming with OK. Once defined, the custom toolbar can be shown by right-clicking any toolbar area and selecting it from the list.

**Cut frame** — Cuts the outer frame/border of the marker when the computer is connected to a cutting plotter.

**Cut order set up** — Sets up the cutting sequence for pieces to be cut by an auto-cutter; clicking the icon shows the cutting sequence on the pieces, and holding Ctrl while clicking a piece opens a Cutting setup dialog box to configure it.

**Cut Piece** — Cuts the selected piece vertically or horizontally at a specified position (with an optional seam width and half-cut option) so the resulting parts can be placed on markers separately to save material.

**Cut pieces** — Automatically cuts individual pieces when the computer is connected to a cutting plotter.

**Cut pieces in One page** — Used for the special case where a piece spans between the first and second page; the system selects the piece to be cut entirely on the second page instead of cutting part of it on the first page.

**Cut view pieces** — Cuts a pattern piece where it overlaps another piece on the marker. After selecting the pattern and activating the tool, a cut line with rectangular handles on both sides and in the middle appears; dragging a side rectangle rotates the cut line around the opposite rectangle (with the angle shown at Degree and seam allowance input), dragging the middle rectangle moves the cut line, and Vertically/Horizontal buttons force the cut line to those orientations before confirming with OK.

**Cut, Drill, Drill M43,M44,M68** — Mode options that display drill or notch-type internals according to their configured drawing properties.

**Cutter stripe setup** — Sets up striping information for pieces destined for an auto cutter. After striping the pattern normally, clicking this icon shows already-striped pieces in orange (meaning they still need to be stripped by the auto cutter) and unstriped pieces in grey; clicking a striped (orange) piece toggles it to blue (meaning stripping is not needed for the auto cutter), and clicking again toggles it back to orange. Adjustment is enabled via Option > Adjust strip.

**Cutting Seg.** — Defines the length to be cut per cutting segment.

**Default** — Under Show Parameters, lets you select a new default font for the item.

**Define Baseline** — Creates reference alignment lines (vertical and horizontal) on the marker that can be used when placing pieces, aligning pieces when moved, checking pin positions, and printing baseline positions/distances (commonly used for pearl, cap nesting, or high-low marker making). Lines can be added, deleted, or dragged into position.

**Define Enter line** — Defines the position where pages are split during printing/plotting, or the space between two markers. The line can be added with a position and space value, shown on the marker, dragged to adjust, and previewed via MultiLine Marker Preview.

**Define layer** — Defines which part of two overlapping pieces should be reserved or discarded when plotting/printing. Clicking a piece sets it as the top (1) layer, which plots entirely, while the other piece is automatically set as the bottom (2) layer, whose overlapped area (shown with a grey line) can be excluded from output or plotted as a dashed line. Layer numbers can be changed by clicking inside a piece, following the rule that the piece with the smaller number overlays the piece with the bigger number.

**Define Marker** — Edits or changes parameters of the current marker such as marker size, number of plies, and marker border; opened via the icon or the Ctrl+M shortcut, which pops up the Define Marker dialog.

**Define Marks** — Available in the Stripe dialog box after selecting a piece; opens the Define Stripe Marks dialog for setting up marks on the piece.

**Define Material** — Opens the Stripe Definitions dialog box, allowing the user to set stripes and grids to match the real material being used.

**Define Material Pattern** — Displays a material/fabric pattern image on the marker for reference. Lets the user select and open an image file to show on the marker, and later alter or delete the displayed pattern.

**Define Material Toolbar** — Sets the size of the material toolbar. Accessed via Option -> Toolbar and Windows -> Define Material Toolbar, where the user inputs a number and clicks OK.

**Define Stripe Marks** — A dialog used to create and manage marks that link matching positions between pieces so that stripe/grid designs align correctly across pieces, using parameters such as Pattern, Size, Add, Edit, Delete, and Clear.

**Define Stripes** — Defines stripes, grids, stamps, or imitation designs on fabric so that a piece can be placed with a specific design in a specific position, ensuring pieces are cut correctly and the design remains complete across pieces.

**Delete** — Removes the selected file from the loaded file list.

**Delete Pieces** — Deletes the selected piece from the piece window or marker, prompting whether to delete the same piece across all sizes, only the selected size, or to cancel the deletion.

**Depart with multiple material** — Saves the currently opened marker as multiple material marker files according to cloth color and unit settings. You add material numbers, input the quantity of each size per material number, auto-depart or manually depart sizes, then save the resulting files, which each group pieces sharing the same material number.

**Depart with single material** — Saves the currently opened marker as single-material marker files split by size: you set up the marker, use Auto Depart (or manual departure) to assign size quantities to each marker, then save the resulting departed files.

**Des** — Defines the length between dashes and their intervals, between dots and their intervals, and between dash-dot segments and their intervals for line styles.

**Description** — Opens a popup list of items that can be selected to display on the marker's border; allows editing, deleting, changing line style, and setting font directly, with a preview column showing the result.

**Description at head** — Plots the marker's description text before plotting the marker itself.

**Draw** — A Mode option that displays internals such as drill or notch according to the drawing mode/property set for them in the Internals settings.

**Draw all pieces then cut** — Draws all piece outlines first, then performs the cutting.

**Draw pieces Border when Cutting** — Draws the piece border while cutting; if not selected, no piece border is drawn during cutting.

**Draw rectangle** — Draws a rectangle on the marker that can be printed or plotted along with the marker. To draw, select the tool, click on the marker and drag; to delete, use the move tool, hover over the rectangle's outline until the cursor turns into an arrow, then right-click and choose delete.

**Duplicate All** — During manual marking, mirrors and copies the position of already-placed pieces onto the remaining pieces of incomplete sets, aligning them flatly according to the completed parts. If piece quantity is insufficient, depending on the 'Not duplication when insufficiency' parameter setting, it either warns and blocks duplication or duplicates anyway (resulting in a negative count in the Size List).

**Duplicated Reverse All** — Duplicates the remaining pieces referring to already-completed pieces, laying them on the marker rotated 180 degrees, unlike Duplicate All which lays them flat.

**Duplicated Reverse Selected** — Duplicates the remaining pieces for a selected set of reference pieces (selected via click or Ctrl+click), laying them on the marker at 180 degrees in the same nesting status as the completed pieces.

**Duplicated Selected** — Duplicates the remaining pieces for a selected set of reference pieces (selected via click or Ctrl+click), aligning them flatly on the marker in the same nesting status as the completed pieces.

**Edit** — Opens the Edit a Mark dialog to modify the currently selected stripe mark.

**Edit Weave Line** — Adjusts the weave line of a selected piece. Opened via Piece - Weave Line, it provides arrow controls to reposition the line, Lengthen/Shorten controls to resize it, and Vertical Center/Horizontal Center controls to center it, with Apply to confirm and close the dialog.

**Edit Weave Line of All pieces** — Adjusts the weave line for all pieces at once. Accessed via Piece menu, the dialog provides Vertical Center and Horizontal Center options to center the weave line for all pieces both vertically and horizontally.

**Embedded Pattern** — Compacts overlapped patterns on the marker into tighter spacing. Clicking the icon opens a 'compact overlapped patterns' dialog where a mode is selected: Normal runs automatically until finished with no time limit, Advanced allows setting a compact time and stops when finished or when the time runs out, and the process can also be stopped manually.

**Estimate Material** — Estimates material usage for cap nesting. Accessed via Nesting -> Estimate Material, opening a dialog where the user defines Unit and Wastage, then clicks Calculate to compute material usage for each size and mode (Normal, Reverse, Interleaving, and their @ variants), showing values such as count, length, width, consumption, waste, and material consumed per size, with an option to output the results when exporting to a text file.

**Exit** — Ends the operation of the system (shortcut Alt+F4). Can also be triggered by clicking the close button at the top right of the system interface.

**Export Bitmap** — Exports the entire marker, along with certain information, as a .bmp bitmap image file so that people without CAD software can still view the marker; the bitmap's dimensions are edited before export, with the bitmap width corresponding to the marker length.

**Export file** — Exports the data as a *.txt file so the result can be checked on any computer.

**Export to File** — Consolidates the plotting output into files saved to a specified folder instead of sending directly to a plotter; done by selecting Output to File in the Plot dialog, browsing to a save location, entering a filename, and saving.

**File (parameter)** — A parameter in the Order for marker making dialog that lists the path and filename of the current pattern.

**Fill color** — Fills pieces with color; the fill color itself can be changed via the Color command in the Option menu.

**Fix Marker Length** — Locks the marker length at its current value so it will not change; the length can later be altered via the Marker Definitions dialog.

**Fix Piece Position** — Fixes one or more patterns in place on the marker so their position and orientation cannot be changed, dragged, or rotated during marker making, forming a single group when fixed together. Select the patterns and click the Fix Piece Position icon.

**Fixed Deg** — Sets the fixed rotation angle applied to a piece each time the 1 or 3 key is pressed.

**Fixed Moving** — Sets a fixed step distance that a piece moves each time an arrow key (left/up/down/right) is pressed.

**Flip horizontally** — Flips the selected piece(s) on the marker horizontally, provided the piece's Limit Marking is set to 2-way, 4-way, or Any with flip allowed; triggered by clicking the icon or pressing key 9.

**Flip Piece** — Flips the selected piece up/down or left/right, either flipping it directly or duplicating it and adding the flipped duplicate to the piece window. If the piece is already on the marker, flipping only creates a new piece added to the piece window.

**Flip vertically** — Flips the selected piece(s) on the marker vertically, provided flip is allowed in the piece's Limit Marking settings; triggered by clicking the icon or pressing key 7.

**Folded mode** — Specifies whether a piece can be folded, using Top/Bottom options for folding up and down (useful for tubular material alignment) or Left/Right options for folding along the left or right border.

**Font on Woveling Upwards always** — When ticked, keeps the font on the weave line always oriented upward; when unticked, the font may be shown in the opposite orientation.

**Global Internals【T】** — Alters internal attributes (such as notches, buttons, drills) across multiple pieces at once, unlike the Internals command which only edits one internal on one piece. Options let the user target the current size, all sizes of the current piece, or all pieces/sizes, and change original notch/drill types into new types with new parameters (length, width, radius, distance).

**Group** — Groups two or more selected pieces together so they can be moved simultaneously as a single unit; select pieces with a marquee, then click the icon to group them.

**Group Auto Nesting** — Used for cutting plotter output, creating a grouped marker according to paper size. Operated via Nesting -> Group Auto Nest, entering group and interval values in the dialog box, then clicking OK.

**Horizontal** — Sets the horizontal attribute of a stripe mark; selecting 'Set offset' requires entering the distance from the origin point in the offset field.

**Horizontal angle** — Sets the inclination angle between a stripe line and the horizontal line, with counter-clockwise defined as the positive direction.

**Horizontal distance** — Sets the distance between two horizontal stripes.

**Horz Shrinkage, Horz Scaling, Vert Shrinkage, Vert Scaling** — Fields for inputting percentage values that cause the piece to shrink or scale relatively (horizontally/vertically) before being placed on the marker.

**Information** — Displays information about a loaded file, including file name and save location, load time, last modified time before loading, file length (in bits), and file ID (which changes if the DGS file was modified or associated in GMS).

**Internals** — Revises the attributes of all internals on a piece, such as notches, holes, and buttons, allowing the user to check and change their size, type, etc. The user selects a piece, opens Piece - Internals, selects an internal, edits its attributes (type, length, width, radius, distance), and applies the changes; includes Previous/Next navigation, Number (reorder), Delete, and Apply options.

**Layout mode** — Selects whether the marker layout is Single or Faced; if Faced, requires selecting a Folded mode (top, bottom, or left).

**Left** — Defines the left margin of the marker border.

**Left fold** — Folds a piece along its left side for tubular marker nesting where the piece requires left-right symmetry; the piece appears folded in half and stays on the folded side of the marker.

**Length** — Defines the marker length. This value is only a reference for the longest cutter length and can be changed during marker making as needed.

**Limit Flip** — Restricts the use of flip tools (flip horizontally, flip vertically, flip piece) according to the Limit Marking settings in Piece Information. When on (icon concave), flipping via keys 7/9 is governed by the piece's Quantity/Attribute/Limit Marking settings; when off (convex), pieces can be flipped without those limits.

**Limit Marking** — Controls how a piece may be rotated/flipped during marker making for material efficiency: 'Any' allows random rotation, 'Flip allowed' permits flipping, and 'One-way', 'Two-way' (180° rotation), or 'Four-way' (90° rotation) restrict rotation for one-way materials or strict stripe/grid layouts.

**Limit Rotation (L)** — Restricts the use of rotation tools (rotate by any angle, rotate 90 degrees) according to the Limit Marking settings in Piece Information. When toggled off (icon convex), pieces can be rotated freely; when on (concave), rotation follows the limits set for the piece, and hotkeys 1/3 (rotate by fixed degree) or 5 (rotate 90°) behave differently depending on this setting.

**Load** — Opens the Order for marker making dialog box, allowing the user to select nest files such as DGS, PDS, or PTN to load into the marker.

**Marker border** — Used to define margins for damaged material borders so that pieces will not be placed in the damaged area, with Left, Right, Top, and Bottom sub-fields defining each margin.

**Marker definition** — Dialog box used to configure settings for a new marker, such as size, comment, plies, layout mode, and borders.

**Marker length** — When selected, allows the marker to continue being made when the actual marker length exceeds the set marker length; otherwise, marker making stops once the set length is exceeded.

**Marker selection** — Lets the user pick up a previously used reference marker listed under the Comment field.

**Marker Text** — Inserts text into a blank area of the marker via a Marker Text dialog box that appears when clicking on the blank space; requires 'Show Marker Text' to be enabled under Options to be visible.

**Marker Text above pieces** — Used with the marker text tool; when ticked, text placed on the marker is not covered by overlapping pieces.

**Material** — Defines the material of the selected piece; entering a different value here replaces its material.

**Measure** — Measures the distance between any two points on the marker by clicking and dragging from a start point to an end point; the DX and DY distances are shown in the status bar.

**Merge** — Merges two marker files into a single marker; both markers must have the same width. Open a marker file, choose File > Merge to open the union marker file dialog, then select another marker file from the list, which is appended after the current marker.

**Mixed color shade（Portrait X）** — When selected, all pattern pieces are nested according to a set method (way 1 of X set), arranged from left to right in portrait orientation.

**MutiLine Marker Preview** — Used to review the printed effect of a Multi-Line Marker before printing, via File - Print Marker - Multi Line Marker Preview. Line change locations can be set via Marker - Define Enter Line.

**MutiLine Marker Print** — Used to print the Multi-Line Marker. Accessed via File - Print Marker - MutiLine Marker Print, then setting parameters in the dialog box and clicking OK.

**Name** — Used to input letters or numbers to name a stripe mark.

**Nest** — Nests all pattern pieces when using cap nesting. Supports 'Not Reverse Piece' (no-distance nesting when mode is set to Normal, Interleaving, or @Interleaving, though distance can also be selected) and 'Reverse Piece' (for Reverse or @Reverse mode, with optional no-distance nesting). Also supports nesting integrity pieces, where remaining pieces that don't form a line can be nested together or nested last. To operate, click 【Cap nest】--【Nest】, choose 【Not Reverse Piece】 or 【Reverse Piece】, then click OK to let the system nest automatically.

**New** — Creates a new marker file. Operation: click the icon to open the Marker Definition dialog to set marker parameters, confirm to save the file, load pattern files (PDS or PTN), configure the Order for Marker Making dialog, then confirm to build the new marker.

**New single Material Calculation file** — Calculates instantly the total cloth quantity needed for an order using a single material. You create a new calculation file, enter the total set quantity, auto-depart sizes into markers (specifying sets per marker, max plies, and whether same size is allowed in a marker), nest markers automatically or manually, and save; the system keeps whichever nest (auto or manual) gives higher efficiency and computes best fabric usage, with results exportable to a txt file.

**Next** — Steps forward through the notches, drills, or marks listed in the Stripe dialog box to select the desired one.

**No Bind Pattern** — The opposite operation of Bind Pattern; removes the bind property from previously bound patterns. Select the bound pattern(s) and click the No Bind Pattern icon.

**No Cutting Seg.** — Defines, by input value, how long a segment can be cut and how long must remain uncut, based on the line shape, used to control segmented cutting.

**Not duplication when insufficiency** — When ticked, prevents duplicating the marker (including reverse duplication) when the piece quantity is insufficient.

**Not need press mouse when move piece** — When ticked, allows moving a piece without needing to hold down the mouse button.

**Not place piece when overlapped** — Available only when 'Not need press mouse when move piece' is ticked; prevents a piece from being placed if doing so would cause it to overlap another piece during marker alignment.

**Only change current piece's status** — Controls how overlapping pieces are shown during nesting: if selected, only the later-placed overlapping piece is shown hollow with a blue outline while the earlier piece stays filled; if not selected, both pieces are shown hollow, with the later piece outlined blue and the earlier piece outlined red.

**Only nesting main** — When selected, only the main marker pattern pieces are nested; when not selected, pieces are nested together with the pattern on the piece list.

**Open** — Opens a marker file that has already been finished. Operation: click the icon to open the 'Open marker file' dialog, select an existing .MKR file, then press Enter, click Open, or double-click the filename.

**Open a pattern file** — The File toolbar command used to access file menu functions such as New, Open, Save, and Print, as well as setting up, altering, and checking piece information.

**Open HP-GL File** — Opens an HP-GL format file exported from other CAD software so it can be output through a plotter. Accessed via File - Open HP-GL File, selecting the file in the dialog, then plotting it via the Plot command.

**Open Multiple Material Calculate File** — Opens a previously saved multiple-material calculation file (or a marker file directly) for review.

**Open Multiple Material Calculate File (calculation)** — Calculates instantly the total cloth quantity needed for an order across multiple different materials; setup mirrors the single-material calculation file process but adds an 'add material' option to handle multiple materials.

**Open Sigle Material Calculate File** — Opens a previously saved single-material calculation file (or a marker file directly) for review.

**Open/Close Size List box** — Opens and closes the Size List Box. The tool appears concave when the size list box is open and convex when it is closed; this tool is only active if the Piece Window is open.

**Options Menu** — A menu containing commonly used show/hide commands, including Parameter, Limit rotation, Limit flip, Round after rotation, Colors, and Fonts, many of which also have shortcut icons in the utility toolbar.

**Order for marker making** — A dialog box that lists loading order/settings for pattern files; used when loading, viewing, or double-clicking a file to alter its options such as order, pattern, customer, and material.

**Order, Pattern, Customer and material (parameter)** — Parameters in the Order for marker making dialog; if these have already been defined in Global Info, they do not need to be renamed here.

**Order, Pattern, Size, Material** — Four informational items already set in the style/piece information from PDS or GGS; they cannot be changed in this dialog but can be edited in the 'Order for marker making' dialog when loading the file.

**Output to DXF** — Saves the marker in DXF format so it can be used by other CAD systems, enabling compatibility with other CAD software.

**Overlapped checking** — Checks the overlap value when two pieces overlap. Click the tool, then click on an overlapped piece to see the maximum overlap value between it and the other piece.

**Paper Size** — A dropdown in the Plotter dialog used to select the paper type/size, or define a custom size via the Custom option.

**Parameters of Pieces** — Contains default settings such as notch length and width, button radius, and defaults applied when uploading patterns into the marker and auto-adjusting weave lines; values can be edited in text boxes to set new defaults.

**Pattern** — Shows and lets the user select the style name of the currently loaded piece, as previously entered in Piece Information within DGS.

**Perimeter** — Displays the perimeter of the selected piece.

**Piece Info** — Accessed via Ctrl+I, this command lets you view and edit information for the current size of the current piece (such as dimensions, quantity, attributes). Select a piece and size, open the dialog, edit the relevant option's values, then click Apply to confirm changes, which affect nesting accordingly.

**Piece menu（Ｐ）** — A menu containing commands related to the operation and attributes of pieces, such as Pieces Info, Rotate Pieces, and Internals parameters. Commands like Information, Flip Piece, Rotate, Cut, and Delete also have shortcut icons on the pieces toolbar.

**Piece Name** — Defines the name of the piece; renaming it replaces the original name.

**Piece name, Code, Description** — Three items set in the style/piece information from PDS or GGS; they can be input or revised in the 'Order for marker making' dialog when loading pattern files.

**Piece on Marker** — Opens the Show Pieces on Marker dialog, letting the user select specific information about pieces to display on screen and export together with the marker files.

**Piece on marker bottom** — Selects all pattern pieces that are folded on the bottom of the marker.

**Piece on marker Left** — Selects all pattern pieces that are folded on the left of the marker.

**Piece on marker top** — Selects all pattern pieces that are folded on the top of the marker.

**Place pieces to aided marker** — Places pieces from the piece box onto the auxiliary marker. Clicking the icon opens a dialog where you select a specific size or all sizes, click Put to move them onto the auxiliary marker, then click Close.

**Plies** — Shows the number of plies in the spreading for the piece; this value can be checked or edited by clicking the associated icon.

**Plot** — Plots the pattern at true size (1:1) using a plotter connected via serial port/LPT or over a network. Opens the Plot dialog where Setup configures the plotter, paper size, edges, and port.

**Plot auxiliary line as** — Sets the style used when plotting auxiliary lines: Solid, Dashed, Dotted, Dashed-Dotted, or Original.

**Plot covered piece's border as** — Sets the style used when plotting the border of a covered (overlapped) piece: Solid, Dashed, Dotted, Dashed-Dotted, or None.

**Plot Marker Border** — Plots the marker together with its border.

**Plot Preview** — Shows a preview of how the marker will be divided into pages for plotting, allowing the user to select specific pages before sending them to plot.

**Plot Scale** — A Plot dialog option that plots the piece at a percentage ratio between a scaled size and the real size.

**Plot selected pages** — Sets the length and specific pages of the marker to be plotted.

**Plot stripe in border only** — Plots the stripe line only on the marker's border.

**Portrait/Landscape** — Options in the Plotter dialog used to select the orientation direction for plotting.

**Prev** — Steps backward through the notches, drills, or marks listed in the Stripe dialog box to select the desired one.

**Preview** — Used to check the printing result of the marker before actually printing. Accessed via the print preview icon on the file toolbar or File - Print Marker - Preview; if the preview looks correct, the user clicks OK.

**Print** — Outputs the marker to a printer in reduced (small) proportion. Accessed via the plot icon on the file toolbar or File - Print Marker - Plot, then confirming in the Print dialog; paper direction can be set via Property - Paper.

**Print File Setup** — Defines a file in Word or Excel format to be used under the printed marker, normally used with Multi-Line Marker Print. The user browses to and opens a file, selects it as the Print File, sets page margins, and clicks OK.

**Print Information Setup** — Sets up the marker information to be displayed/printed, such as All Info and Size Info items, via File - Print Information - Setup, using the Nesting Information dialog box where items can be ticked, edited, reordered, or deleted.

**Print marker** — Exports and prints a small-scale version of the marker through a printer. Click the icon to open the Print Marker dialog, choose print options, and click OK.

**Print preview** — Previews how the marker will look when printed; if satisfied, you can proceed to Print Marker from the preview screen.

**Print set** — Used for setting the page border, printer type, and print direction.

**Print setup** — Used to set the contents to be included in the 'order for marker making'; blue color indicates selected contents.

**Printer Setup** — Used to configure the printer type, paper size, and print direction for outputting markers.

**Quantity** — Defines the cut quantity of the piece on the marker. This number is displayed in the size list as a counter and decreases during marker making until all pieces are completed or placed; if set to 0, the piece will not be read for marker making.

**Rearrange Auxiliary Marker** — Automatically arranges pieces on the auxiliary marker according to size; only works on the auxiliary marker (shortcut F3).

**Redo (Ctrl+X)** — Re-applies operations that were previously undone, and can be used repeatedly to redo multiple operations.

**Reference Marker** — Opens a previously finished marker file to use as a reference, allowing a new marker to be aligned based on it.

**Refresh** — Clears useless points created while running the program (shortcut F5).

**Remainder** — Shows the quantity of pieces that have not yet been placed on the marker.

**Remove selected pieces (Delete or double click)** — Removes selected pieces from the marker and returns them to the piece list, without permanently deleting them. Select pieces on the marker with the move-selected-piece tool, then click the Remove selected pieces icon, use Marker > Clear selected piece, press Delete, or double-click the pattern on the marker with the move tool active.

**Report** — Displays the current marking solution's statistics, such as efficiency, complete sets, plies, and size/quantity per set. Accessed during or after marker making via Nesting -> Report, closed by clicking OK.

**Reverse Piece Mark** — When selected, displays a reverse marker (such as 'REV') on reversed pieces during nesting so that reversed pieces are visibly identified; unselected pieces show no such mark.

**Reverse sets** — Used for nesting under the 'one size one direction' concept; shows the quantity of reversed pieces.

**Right** — Defines the right margin of the marker border.

**Right fold** — Folds a piece along its right side for tubular marker nesting where the piece requires left-right symmetry; the piece appears folded in half and stays on the folded side of the marker.

**Right limit as base line** — When manually finishing a marker, this option aligns the right border of the marker as the reference base line.

**Rotate 180 Degree** — Rotates a pattern 180 degrees when its grain line is set to Double-way, Four-way, or Any-way. Select the pattern and click the icon to rotate; right-click or press 5 to instead rotate it 90 degrees.

**Rotate 180 Degree for All Piece of a Set (F4)** — Rotates all pieces belonging to a set 180 degrees for the currently selected piece(s) on the marker. Used by selecting a pattern on the marker and pressing F4 or choosing Nesting -> Rotate 180 degree for all piece is a set.

**Rotate 90 degree** — Rotates the selected piece on the marker by 90 degrees when the icon is concave and the piece's Limit Marking is set to Four-way or Any; can be triggered by clicking the icon, right-clicking the mouse, or pressing key 5 on the numeric keypad.

**Rotate 90 Degree Anti-clockwise** — Rotates a selected pattern 90 degrees when grain line settings (under Pieces Info - Limited Marking) are set to Four-way, Any, or another unselected option. Select the pattern and click the icon to rotate; if the grain line is Double-way, right-clicking or pressing 5 rotates it 180 degrees instead.

**Rotate Piece** — Rotates the selected piece by any angle, either rotating it in place or duplicating it after rotation and adding the duplicate to the piece window. If the piece is already on the marker, rotating creates a new piece added to the piece window.

**Rotate piece any angle** — Rotates the selected piece by a user-specified degree and direction, entered in a pop-up dialog box, when the tool icon is set to concave.

**Rotate Piece by hot key according weaveline limit** — Controls the rotation hotkey behavior (key 5 or right-click): when unticked, rotates the pattern 90 degrees; when ticked, rotates the pattern 180 degrees respecting weave line limits.

**Round After Rotation** — A setting that affects mouse-based pattern rotation. When enabled via Option > Round after rotation, rotating a pattern snaps it to the nearest of four directions (0°, 90°, 180°, 270°) when the rotation angle is within about 6 degrees of one of them.

**Same proportion marker and aided marker** — Displays the major marker and the auxiliary (aided) marker's pieces in true proportion to each other. Clicking the tool toggles this proportional display on and off.

**Save** — Saves the marker to a specified path for later use. If the .MKR file was previously saved, it saves under the current file; if saving for the first time, use 'Save as' instead. The .MKR extension is added automatically.

**Save as** — Saves the current calculation/marker file under a new filename and path chosen by the user; the system automatically appends the .MRK extension to marker files.

**save current nesting** — Used when a single marker file's layout is placed into different markers, to save the current nesting arrangement.

**Save current nesting only** — If ticked, only the nested pieces of the current marker are saved and un-nested pieces are excluded; if left unticked, all pieces (both aligned and non-aligned) are saved.

**Save current Solution** — Dialog for saving the current marker under a filename you type in or select via Browse; when saving similar markers repeatedly the system appends a dash and number to the base filename (e.g., 2035.mkr, then 2035-1.mkr).

**Scale** — A Plot dialog option that plots pieces at true 1:1 proportion.

**Select all fixed pieces** — Selects all pieces on the marker that have been fixed (locked) in place.

**Select All Piece, Current Size** — Selects all pieces on the marker that share the same size as the currently selected piece.

**Select All Pieces** — Selects all pattern pieces currently placed on the marker.

**Select colors** — Specifies different colors for the system interface, all sizes, and all sets; opened via the icon, Options menu > Colors, or the shortcut Alt+O+C, which opens the Select Colors dialog for configuring colors for general objects, sizes, sets, and style colors.

**Select Current Piece, All size** — Selects the currently selected piece across all of its sizes.

**Select Current Piece, Current Size** — Selects all instances of the currently selected piece that are in its current size.

**Select fonts** — Selects the fonts used for the interface displayed on the marker and determines the fonts used when printing and outputting; accessed via Options > Fonts or Alt+O+F, opening the Font dialog to choose font, text size, and ignored text size.

**Select piece** — Used to select and move pieces in the marker: click to select a single piece, drag a marquee or Ctrl-click to select multiple pieces, rectangle-marquee sizes in the size list to auto-align selected pieces onto the marker, drag to move a piece, or double-click to return a piece to the piece window. Additional shortcuts (Ctrl or Shift + double-click on a size) trigger automatic nesting of pieces for a pattern or size, filling remaining marker space with pieces from other patterns/sizes where possible.

**Selected marker** — When selected, allows choosing the last defined marker length and width from a list; the size becomes the default for the next marker, letting users input a commonly used marker size.

**Self-adjusting of overlapped pieces** — When ticked, pieces that overlap are automatically nudged/adjusted apart during manual marker making.

**Separate pieces according to material** — Saves the currently opened marker as multiple marker files grouped according to material, placing pieces that share the same material onto one marker each.

**Set** — Allows input of the set number for all sizes; e.g., if size L quantity is half of size M, size M is 2 sets when size L is 1 set.

**Set All Piece's Count to 1** — Sets the quantity of all pieces to 1, displayed in the Piece Window. The original quantities can be restored by reopening the pattern file and confirming the Order for Maker Making dialog.

**Set number using letter** — When ticked, the set is identified by a letter instead of a number.

**Set symmetry cut** — Sets the symmetry cut property for a pattern piece. Accessed via Cutter -> Set Symmetry Cut, opening a dialog where the user clicks an arrow to confirm the start point; a Reset option removes the symmetry cut property, and when exporting to an auto cutter with the Symmetry Cutter print/plot parameter enabled, the pattern is cut symmetrically.

**Setup** — Sets up parameters for cap nesting pieces, similar to the Order for Marker Making dialog, including counts per size, quantity of pieces, material, and nesting mode (Normal, Reverse, Interleaving, etc.) defined individually for each piece. Accessed via Cap Nesting -> Setup, opening the Para Setup dialog where Quantity, Sets per Unit, and nesting Mode are entered.

**Setup Parameters** — Sets the speed and related parameters for the automatic marking process, limiting how the whole auto-nesting operation runs before it starts. Includes the 'Fill Hole of Nested Pieces' option, which, at Normal or Slow speed, intelligently inserts small pieces into gaps between nested pieces.

**Show all pieces** — Displays all pieces currently placed on the marker when the icon is clicked.

**Show all pieces in aided marker** — Displays all the pieces placed in the aided marker when the tool is clicked.

**Show auxiliary line as** — Changes how auxiliary (assistant) lines inside a piece are displayed: Solid, Dashed, Dotted, Dashed-Dotted, or Original.

**Show Base line** — Shows or hides the base line on the marker.

**Show bottom limit** — When ticked, displays the bottom limit line on the marker.

**Show folded border of piece** — When ticked, displays the folded line within a piece.

**Show Full length marker** — Displays the marker at its full length when the icon is clicked.

**Show last right limit** — When ticked, after nesting and saving a marker, then re-nesting a second time, shows the end limit line and turns the marker green, stopping at its original position, allowing comparison of marker length between the first and second nesting attempts.

**Show marker by width** — Displays the marker at its full width when the icon is clicked.

**Show marker Gauge** — Opens or closes the marker gauge display. Clicking the icon shows the gauge, and clicking it again hides it.

**Show Marker Text** — Shows or hides the marker text, allowing it to be displayed and edited.

**Show Marker text According to proportion** — When ticked, marker text and piece text are displayed scaled to the marker's proportion; when unticked, they are shown at real size.

**Show Marker's Pattern** — Shows or hides the material pattern displayed on the marker.

**Show overlap status by virtual border** — Adds a virtual border around patterns for overlap checking; if virtual borders overlap, the pattern's color changes and appears without a color fill.

**Show Piece's Description** — When ticked, the piece's description text is displayed on the piece.

**Show Piece's Pattern** — Shows or hides the material pattern displayed on the piece.

**Show pleat and dart with line** — When ticked, darts or pleats are displayed with a line; when unticked, the dart/pleat line is hidden.

**Show size at head** — When ticked, the size number is shown before the piece quantity in the size box.

**Show stripe** — Toggles the display of stripes on the marker on or off via the Options menu.

**Show whole aided marker** — Displays the entire aided marker when the tool is clicked.

**Show width of aided marker** — Displays the aided marker at its maximum width when the icon is clicked.

**Show zero pieces** — When selected, displays pieces whose quantity is zero in the piece window; if not selected, such pieces are hidden from the piece window and size box.

**Side** — Defines whether the selected piece is a single piece or has a right/left attribute. A single piece defaults to this setting; an even-numbered piece can be set to right or left.

**Single Click Piece list to Nest Piece** — When ticked, a single click on a piece in the Size box places it directly into the marker; otherwise a double click is required.

**Size** — Selects the size to which the defined stripe mark applies.

**Size Exchange** — Replaces one or more sizes on an already finished marker to improve efficiency without needing to redo the whole marker. After selecting the sizes to exchange and confirming, any resulting overlaps or internal issues must be adjusted before saving the marker under a new name.

**Size name** — Displays the size name for all sizes.

**Specific Rotation** — Rotates a pattern around a clicked axis point. If the grain line option is not selected, the pattern can be rotated freely; if selected, rotation is constrained to 180 degrees (Double-way), 90 degrees (Four-way), or free rotation (Any) around that axis point. Operated by clicking the tool, then clicking and holding on the pattern to rotate before releasing at the desired angle.

**Specify Directory** — Saves all files to a specified directory so files can be found even after a wrong operation; prevents patterns from being saved elsewhere and reminds the user to save to the appointed directory.

**Start AutoNesting** — Starts the automatic marker-making (nesting) process. When complete, a Check Solution dialog appears; if some pieces were already manually placed on the marker, the system aligns the remaining pieces and continues nesting until stopped.

**Status main** — Clicking the small triangle button opens a list of options that can be selected to display on the status bar.

**Stop** — Stops the automatic nesting (marking) process. After starting AutoNesting, clicking Nesting -> Stop brings up a Check Solution dialog box; nesting can be resumed later by clicking Start AutoNesting again.

**strip adjust** — An option selected in the strip dialogue table used to choose which mark sign will be assigned to the currently selected notch or drill.

**Stripe only in a set** — When multiple sets exist for one size, this option lets each size be striped separately, improving nesting efficiency.

**Supernest** — An automatic nesting mode that achieves higher efficiency than manual nesting in a short time. Used by loading the pattern file, setting the marker width, then Nesting -> Supernest, entering a time (e.g., 3 or 10 minutes) in the Set Supernest dialog, and clicking OK to start; includes parameters for time limit, efficiency-based continue/exit behavior, avoiding color shade (horizontal, vertical, or mixed), allowed slant angle, and whether overlap between pieces of different sets is permitted.

**Text** — Adds text onto a piece on the marker; clicking the piece opens a Text dialog box where the text is entered and confirmed. Includes parameters for adjusting text position (with arrow movement, accelerated by Ctrl), height and angle, font, and an 'All sizes' option to apply the text automatically to all sizes.

**The last five files used before** — Lists the last five files that were opened, allowing the user to quickly reopen one by selecting it from the File menu list.

**Time Nest** — Sets the time limit and efficiency target for nesting. Selecting 'Apply and Continue' makes the system continue nesting until it reaches the highest efficiency marker once the set efficiency is reached; selecting 'Apply and Exit' stops nesting once the set efficiency is achieved.

**Toolbar and Windows** — Controls whether a given toolbar or window is shown or hidden. Accessed via Option -> Toolbar and Windows, then selecting the name of the toolbar; selected toolbars display, unselected ones are hidden (default is shown).

**Top** — Defines the top margin of the marker border.

**Top fold** — Folds a piece along its top side for tubular marker nesting where the piece requires top-bottom symmetry; the piece appears folded in half and stays on the folded side of the marker.

**Total Piece Info** — Allows altering data (such as weight) for all pieces of all sizes at once by inputting values that take effect on each size of each piece.

**Total pieces** — Displays the total area of pieces on the marker.

**Undo (Ctrl+Z)** — Reverts the marker to a previous state, and can be used repeatedly to undo multiple prior operations.

**Unfixed Pattern Position** — The opposite operation of Fix Piece Position; removes the fixed property from previously fixed patterns so they can be moved and rotated again. Select the fixed pattern(s) and click the icon to unfix them.

**Unfold pieces** — Shows a folded pattern piece opened back up (unfolded) after selecting a folded pattern and clicking this icon.

**Ungroup** — Splits apart a previously grouped set of pieces back into individual pieces; select the grouped pieces and click this tool.

**Unit** — Used for selecting the area unit or length unit shown in the table.

**Up、Bottom、left、Right** — Moves the selected pattern piece up, down, left, or right, equivalent to the numeric keypad's 8, 2, 4, 6 direction functions.

**Use software broken line** — Used to plot dashed lines in software when the plotter hardware itself cannot plot broken lines; must be set up in advance.

**Vertical** — Sets the vertical attribute of a stripe mark, working the same way as Horizontal but for the vertical direction.

**Vertical angle** — Sets the inclination angle between a stripe line and the vertical line, with counter-clockwise defined as the positive direction.

**Vertical distance** — Sets the distance between two vertical stripes.

**View** — Displays all the contents of the Order for marker making dialog for the selected file, allowing the user to review or alter it before confirming.

**Virtual Border** — Controls whether the buffer figure is shown on screen; must be ticked to export the buffer figure via a plotter.

**Weave line** — Shows the weave line on pieces when ticked, or hides it when unticked.

**Weight per square centimeter** — Defines the weight of the cloth per square centimeter so the system can calculate the total weight of cloth used by all pieces of all sizes; input the value and click Recalculate to get the total weight.

**Width** — Defines the width of the marker (material).

**Window Size** — Sets Piece window width, Piece window height, and Size list box height by typing new values or using the adjustment slider, affecting the size of the piece window.

**Working directory** — The work path used by the current plotter for network plotter connections; for example, if computer A plots over the network through a plotter connected to computer B, the working directory is the plot folder location on computer B.

**Working units** — Sets the measurement unit used for the marker. Accessible via its icon, the Marker > Work Units menu, or the shortcut Alt+M+W; select the desired unit and click OK.

**X** — Defines the starting position of the stripe in the X (horizontal) direction, measured from the left side of the marker.

**Y** — Defines the starting position of the stripe in the Y (vertical) direction, measured from the top side of the marker.

**zoom** — Used for adding shrinkage or scaling to a marker that has already been made.

**Zoom in** — Magnifies a specified area of the marker; click or drag a rectangle marquee around the area to zoom in, and right-click to return to the previous view. Pressing the space bar while using the piece-select tool switches to this Zoom in tool.

**Zoom Out** — Returns the pattern displayed in the main marker to its previous (unzoomed) proportion.

**Zoom Out Aided Marker** — Zooms the pattern in the aided marker view back out to the previous proportion. Clicking the icon repeatedly steps back through zoom levels until it turns grey, indicating no further zoom-out is possible.

**Zoom pieces** — Zooms the whole selected pattern in or out. After selecting the pattern, a Scaling pattern dialog appears; entering '+' zooms the pattern out and entering '-' zooms it in, then clicking OK applies the change.
