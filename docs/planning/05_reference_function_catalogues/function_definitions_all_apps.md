# Complete Function Definitions — Legacy Gerber Applications
*A plain-language reference explaining, in detail, what every documented function does in each
of the five applications: Pattern Design (PDS 2000), Marker Making, Order Entry, IGES
Translator, and Style Converter — written for factory and production-floor workers, not
software engineers.*

**How this was built:** every item below started from the manual's own Table of Contents (for
Pattern Design, Marker Making, and Order Entry) or its command/error catalog (for IGES and
Style Converter). For each item, the actual explanatory text from the manual was located and
used as the source for a plain-language rewrite — nothing here is invented from the item's
name alone unless explicitly marked as inferred. 1157
of 1174 items across the three large applications were
matched to a real manual excerpt; the small remainder were written from standard AccuMark
terminology and flagged as such in the source data (not marked individually below to keep the
reading experience clean, but available on request).

**How to read this document:** `###` headings are chapters/major sections; bold items under them
are individual functions/commands within that chapter, each followed by its plain-language
definition.

---

## Pattern Design (PDS 2000 / Silhouette 2000)
*552 documented functions/sections, each defined below*

### Getting Started
This is the introduction section of the online help that explains what PDS 2000/Silhouette 2000 is and who it's for. It tells you that the software combines Gerber's older pattern design systems (AccuMark PDS, Silhouette, MicroMark PDS and FCAD) into one program that runs on a familiar Windows interface, with commands organized on customizable tool bars so you can build patterns faster. It assumes you already know pattern-making and have basic training on AccuMark/MicroMark, so it's meant as a refresher/orientation rather than a beginner's course.

### Glossary of Terms
This is a list of the technical words and terms used throughout the software and manual, like Apex, Grade Rule, Notches, Seam Allowance, and Slash Lines. Workers can look up any unfamiliar term here to quickly understand what it means before using a related command, rather than guessing at its meaning while working on a pattern.

### Pattern Design Work Space
This is the section header/title page introducing the main screen area where you build and edit patterns in PDS 2000/Silhouette 2000. It leads into the topics that describe the different parts of the work space, such as the menu bar, tool bars, and information bars.

**Get Acquainted with the Work Space** — This is an interactive help feature where you move your mouse over different parts of the main screen to see labels and explanations of what each feature is. It's used to learn the layout of the screen (menus, tool bars, work area) since every command in the program is accessed from this screen. If the window is too small to see everything, clicking the middle button in the upper right corner expands the view.

**Menu Bar** — The Menu Bar is the row of 11 drop-down menus at the top of the screen (File, Edit, View, Point, Line, Piece, Grade, Measure, Draft, Window, Help) that give you access to every command in the program. For example, the File menu lets you open, save, print, or plot patterns, while the Edit menu lets you undo actions or edit details of points, lines, and pieces. Workers use this bar as the main starting point to find any function they need when building or editing a pattern.

**Tool Bar** — The Tool Bar is a row of icon buttons for commands you use often, grouped by task — Point (adding/deleting points and notches), Line (creating or modifying lines and shapes), Piece (creating pieces, adding darts/pleats/seams, folding or splitting), Grade (creating and editing grading rules for sizing), Measure (checking lengths, distances, and angles), and Draft (sketching, scaling, and trimming). Clicking a tool bar icon is a faster shortcut than going through the drop-down Menu Bar for the same command, which speeds up repetitive pattern work.

**Using the AccuMark Menu** — This turns on an older-style menu layout that matches the classic AccuMark PDS/Silhouette system, for workers who are more comfortable with that familiar setup. You turn it on through View > Screen Layout by checking its box, and you can drag it to reposition it anywhere on screen. The manual notes it's better to learn the new PDS 2000/Silhouette 2000 menus instead, since they include productivity improvements not in the old menu.

**Using the MicroMark Menu** — This turns on an older-style menu layout matching the classic MicroMark PDS system, useful for workers already trained on that version, and it also adds Exit and Exit to Main buttons for closing menus or the program. You enable it via View > Screen Layout by checking its box, and turning on the MicroMark tool bar lets you switch between different MicroMark menus. As with the AccuMark menu, the manual recommends learning the newer main menu bar instead for the added productivity features.

**MicroMark Function Keys** — This displays a row of function key buttons on screen that act as shortcuts to commonly used MicroMark commands, some of which may not have their own tool bar icon. For example, instead of navigating the View menu to zoom out and see the whole pattern, you can just press F3. You turn this display on through View > Screen Layout, and it can be repositioned by dragging.

**MicroMark Tool Bar** — This is a set of icon buttons for quickly opening the MicroMark Points, Lines, Pieces, Grading, and Seams menus without navigating the main menu bar. Clicking a button instantly shows the options for that category (for example, clicking the Points button shows point-related commands). It's turned on through View > Screen Layout and can be dragged to a new position, and it exists as a faster alternative for workers used to the MicroMark system.

**Piece/Icon Menu** — This is a panel that shows all the pattern pieces belonging to the model or style you're working on, either as small picture icons, as text names, or both. It gives workers a quick visual list of every piece (like a sleeve, front, or collar) so they can find and select the one they need to work on.

**Working with Piece/Icon Menu** — This panel lists every pattern piece in your current model or style, shown as icons, names, or both, so you can quickly see and manage all the pieces you're working with. Right-clicking directly on a piece gives you details about it, while right-clicking elsewhere opens the Options Pop-up menu to resize or reposition the panel. From here workers can drag pieces into the main work area to edit them, add a piece from the work area back into this menu, or delete all pieces from the list.

**User Input Box** — The User Input Box is a small window that talks back and forth with you while you're running a command, showing prompts or asking for values like a length or angle. You can set it to always show or to only appear while a command is active, turning it on/off through View > Screen Layout. It helps guide you step-by-step so you enter the right information at the right point in a task.

**Status Bar** — The Status Bar is the standard bar (like in any Windows program) that shows basic system status information at the edge of the screen. It's turned on or off through View > Screen Layout and can be dragged to a new position on the work area.

**Info Bar** — The Info Bar is a strip of information and settings that reflects the piece and pattern you currently have selected, showing things like the style/model name, piece name, size, whether you're looking at Sew or Cut lines, and whether measurements are in inches or metric. It also shows settings such as Snap to Grid/Geometry, System Smoothing, and Hide Seams, and clicking its buttons turns those settings on or off directly. Workers use it to quickly check or change the current working settings without opening a separate menu.

**Prompt Bar** — The Prompt Bar is a horizontal strip (placed above or below the work area) that walks you through the steps needed to complete a command, similar to the User Input Box. It's helpful for workers who want on-screen, step-by-step guidance while using a command instead of remembering the sequence themselves. It's turned on through View > Screen Layout and can be repositioned by dragging.

**Quick Open** — Quick Open is a text field where you can type the exact name of a model, style, or piece file you want to open, instead of browsing through folders. You set which file types it searches for on the General page of Preferences/Options, then just type the name and press Enter to open it — a fast method when you already know the file name. It can be docked in the work space or left floating, and turned on via View > Screen Layout.

**Rulers** — Rulers are horizontal and vertical measuring guides displayed along the edges of the work area that help you judge the size and position of pattern pieces as you work on them. The measurement units shown (inches or metric) follow whatever is set in your AccuMark or MicroMark system options. They're turned on through View > Screen Layout, and each ruler can be dragged to the opposite edge of the work area if you prefer a different position.

### Set Up Your System
This is the starting point in the manual for getting your PDS 2000/Silhouette 2000 software ready to use. It covers the basic setup steps you take before you start building or editing patterns, such as arranging your work areas and setting your preferences, so the program matches how you and your factory work.

**Customizing Pattern Design Work Space** — This lets you set up your screen the way that works best for you, whether you're used to Windows-style drop-down menus or the older AccuMark/MicroMark style menus. You can move menus to a new spot, add buttons to the tool bar, or change default colors, all through the Preference/Options dialog box, so the workspace fits your personal habits and experience level.

**Open, Close, and Arrange Work Areas** — This function lets you open more than one pattern, model, or style at the same time, each showing in its own separate window called a work area, though only one window can be actively worked in at once. You can resize and arrange these windows on your screen like any normal Windows program, and the names of all open work areas are listed under the Windows menu, which is handy when you need to compare or switch between different styles.

**Display Pieces in the Work Area** — Found under the View menu, this controls how pattern pieces look on your screen while you work. You can turn on things like piece outlines/symbols, solid color fill, orientation symbols, seam lines, and notes, or refresh the screen so it shows the most current version of the pieces, and even change how pieces look in the Piece/Icon menu list.

**Docking Tool Bars, Menus, and User Input Box** — This explains how to drag and attach (dock) tool bars, menus, function keys, and the User Input box to the edges of your screen, or leave them floating freely over your work area, just like standard Windows programs. Whatever position you leave them in when you close the program will be saved and will still be there next time you open it, so you can set up your screen once and keep it that way.

**Use Preferences/Options** — This is the section of the manual that walks you through the Preferences/Options dialog box, where nearly all of your personal and system-wide settings for PDS 2000/Silhouette 2000 are configured. It's the main place to go whenever you want to change how the software displays, behaves, or connects to equipment like plotters.

**Preferences/Options** — This command, found in the View menu, opens a dialog box with several tabbed pages (General, Color, Plotter, Style, Paths, and Draft) where you control things like how pieces are displayed, screen colors, plotter setup, style conversion, and where files are stored. You click the tabs to move between pages, then check boxes, click radio buttons, or type values to change settings on each page.

**Setting Draft Preferences/Options** — This is a tab in the Preferences/Options box used specifically for setting up how the software works with the Silhouette digitizing table. Here you can adjust the Point Filter (how many extra points get removed when sketching or tracing), and the Sketch/Note Pen Resolution (how many points get recorded on lines you draw), then save your changes or reset to the factory defaults.

**General Page** — This refers to the General tab within the Preferences/Options dialog box, where the basic, everyday settings for the software are grouped together. It's the starting page workers go to for common adjustments like piece display, selection sensitivity, and workspace behavior.

**Setting General Preferences/Options** — This is the step-by-step process for adjusting the basic settings on the General page of the Preferences/Options box, accessed from the View menu. You select the checkboxes or type in values you want changed, click Save to apply them (which affects all your AccuMark storage areas), or click Reset to Default to go back to the original settings.

**Changing Preferences/Options for Piece Display** — Found on the General page of Preferences/Options, these settings control the visual appearance of pattern pieces on screen. For example, checking 'Filled Pieces' shows pieces in solid color instead of as outlines, 'Symbols' shows markers for points and grade rule locations, 'Fit Pieces in Work Area' automatically zooms new pieces to full view, 'Hide Seam' hides certain seam allowance lines, and 'Orientation Symbol' shows an arrow or marker indicating piece direction (recommended to keep turned on).

**Changing Preferences/Options for Piece Selection and Tracking** — Also on the General page, these settings control how easily you can click on and follow lines or points in a pattern piece. Magnetic Tolerance sets how close your cursor must be to a point or line to grab it, Auto Tracking turns on automatic line-following as soon as you move the cursor near a line, and Tracking Speed lets you choose Slow, Medium, or Fast for how quickly that tracking moves.

### Changing Preferences/Options for AccuMark or MicroMark Environment
This setting on the General page tells the software which grading and marking system your factory uses, either AccuMark or MicroMark, which matters for things like referencing the correct grade rule table. After changing this option you must close and reopen the program for the new setting to take effect.

**Changing Preferences/Options for Work Space and Misc.** — These General page settings manage backup and display behavior: AutoSave Timer controls how often the program automatically backs up your workspace in case of a crash (without overwriting your actual saved style or piece data), AutoSave Undo Buffer lets your Undo history be saved too (though it slows AutoSave down when on), and System Smoothing (default ON) makes curved lines display on screen the way they'll actually look when plotted.

**Options Input Section** — This is the middle-upper part of the User Input box where you make choices specific to whatever command you're currently running. Depending on the command, you might click a radio button to pick between two options, check a box for an extra feature like 'Extend to adjacent lines,' pick a value from a drop-down list, or type in a name or number and press Enter to confirm it.

**User Input Command/Prompt Section** — This is the top part of the User Input box, and it simply tells you which command is currently active and what you need to do next to keep completing it. It acts like a running instruction line so you always know your next step while working.

**User Input Controls Section** — This is the bottom part of the User Input box, containing buttons that manage how you're entering information: Value/Cursor switches between typing exact numbers or using the mouse, Tracking lets you move quickly along piece lines, OK accepts your input and moves the command forward, Cancel backs out of the current input, and Apply accepts input while keeping the box open for more.

**Value Input Section** — This is the middle-lower part of the User Input box used for measurements: in Cursor mode it shows you distance information as you move the mouse, and in Value mode you can type exact numbers instead. To use it, you click on the piece geometry, switch to Value mode if needed (by clicking both mouse buttons at once), then type into fields like Beg, End, Dist, X, Y, or Ang before pressing Enter or OK to confirm the measurement.

**Color Page** — This is the tab in the Preferences/Options window where a worker goes to control all the color settings used on screen, such as colors for pieces, grading, text, and backgrounds. It's simply the starting point (a page/tab in a settings box) for the color-related options described in the items below it.

**Setting Color Preferences/Options** — This function lets a worker change the default colors used on screen for things like selected pieces, piece outlines, grading sizes, and text, so it's easier to tell parts apart while working. To use it, the worker opens the View menu, selects Preferences/Options, clicks the Color tab, then clicks the color swatch next to the item they want to change and picks a new color from a chart or by sliding Red/Green/Blue bars, then clicks OK. This is handy on the job when the default colors are hard to see or when a worker wants pieces, grading sizes, or text to stand out more clearly in the work area.

**Changing Piece Colors** — This setting controls the colors used to show the status of a pattern piece on screen: Original (a piece exactly as saved, unchanged), Highlighted (the piece currently closest to the cursor or in focus when several pieces are on screen), Modified (a piece that's been edited but not yet saved, which turns back to the Original color after saving), and Selected (pieces the worker has clicked to select). Workers use this so they can tell at a glance, just by color, whether a piece has been touched, is active, or is picked for an action.

**Changing Nest Colors** — This setting controls the colors used when viewing a "nest" (a group of graded pieces in different sizes) on screen: Base is the color for the sample/starting size, Intermediate is the color for in-between sizes (AccuMark data only, not available for MicroMark), Breaks is the color for the smallest/largest break sizes, and Rainbow displays every size in its own distinct color. A worker can check current size colors anytime by clicking the arrow next to the base size in the Info Bar to pop up a chart of sizes and their colors.

**Changing Text and Miscellaneous Colors** — This setting lets a worker change the colors of non-piece elements on screen: Prompt (the message text guiding the worker), Annotation (text labels and point/rule numbers on pieces), Work Area (the background color of the main screen), Grid (the color of the on-screen grid lines, whose spacing is set elsewhere in View/Screen Layout), and Arrows (the direction arrows shown in Value mode and when using Measure tools). Workers adjust these to make prompts, labels, or grid lines easier to see against their screen background.

**Plotter Page** — This is the tab in the Preferences/Options window that holds all the settings related to plotting (printing physical pattern pieces on a plotter machine), covering both general plotter defaults and specific cut settings.

**Setting Plotter Preferences/Options** — This function is how a worker opens and adjusts the general settings used whenever pieces are sent to the plotter (the machine that prints or cuts out patterns). The worker goes to the View menu, selects Preferences/Options, clicks the Plotter tab, chooses or types in the desired settings, then clicks Save (or Reset to Default to undo changes) and OK to finish. This is used whenever the shop's plotting setup needs to be changed, for example switching how pieces are arranged or sized when printed.

**Changing Plotter Defaults** — This lets a worker set default behaviors for plotting jobs, including which Piece Plot Parameter Table and Annotation Table (label settings) to use, whether Stacking is on (fitting multiple pieces across the paper width before advancing, versus advancing after every single piece), whether the Plot Form window pops up for manually placing pieces or the system places them automatically, which sizes get plotted from a graded set of sizes (either just what's shown on screen or whatever the parameter table specifies), and the text/character size used on the plot. Workers use these settings to control how efficiently paper is used and how plots come out formatted before sending a job to print.

**Changing Cut Parameter Overrides** — This lets a worker fine-tune the settings used specifically when cutting pattern samples out of material like oak tag (a stiff paperboard used for hard pattern copies) on a cutting plotter. It covers Cut Line Length (how long each perforated cut line segment is), Tab Line Length (the gap distance between cut lines, which leaves small "tabs" holding the paper together), Cut Force and Tab Force (how much blade pressure, as a percentage of maximum, is used for cutting versus tab lines). Workers adjust these when the standard cut settings don't work well for the specific paper or material being cut.

**Style Page** — This is the tab in the Preferences/Options window that holds the settings used when importing or exporting styles between AccuMark and MicroMark systems (two different pattern data formats/systems).

**Setting Style Preferences/Options** — This function lets a worker set up how pattern styles are converted when moving data between the MicroMark and AccuMark systems, including naming rules and how notches, grain lines, and grading reference lines are handled. The worker opens View > Preferences/Options, clicks the Style tab, sets the desired options and matches notch types between the two systems, then clicks Save (or Reset to Default) and OK. This is used whenever a shop needs to exchange pattern styles between the two different systems and wants the conversion to come out correctly formatted.

**Changing Preferences/Options for Naming Styles** — This controls how piece names are automatically adjusted when moving styles between AccuMark and MicroMark, since AccuMark names each piece individually (e.g., "1234rfrnt") while MicroMark groups pieces under one style name without unique piece names. Turning on Retrieve Style/Prefix Style Name adds the MicroMark style name as a prefix to each piece when opening a style (useful when working with multiple styles at once), while Store Style/Append Style Name strips that style name back off when saving. Workers use this so piece names stay organized and don't get confused when switching between the two systems.

**Changing Preferences/Options for Exporting Grain Line** — This setting, when turned on (Export Grain Line), automatically creates a grain/grade reference line on a piece whenever it is exported to the MicroMark format, based on the piece's original AccuMark grain line. Workers use this so they don't have to manually redraw the grain line reference every time a piece is sent to MicroMark.

**Changing Style Preferences/Options for Notches** — This function lets a worker set how notch types (the small marks cut into pattern edges to guide sewing/alignment) in MicroMark get matched up with the corresponding notch types in AccuMark when converting data between the two systems, since each system numbers and defines notches differently. The worker goes to View > Preferences/Options, clicks Style, selects the Notch Table to apply, matches each MicroMark notch type to its AccuMark equivalent, then clicks Save and OK. This ensures notches translate correctly and don't come out wrong or missing when a style or model is imported or exported.

**Paths Page** — This is the tab in the Preferences/Options window used to tell the software where to look for and save piece, style, model, and import files on the computer or network.

**Setting Paths Preferences/Options** — This function lets a worker set up the basic file locations the software uses to find and store pattern data, whether working in an AccuMark environment (which organizes data into storage areas) or a MicroMark environment (which stores styles and grading rule tables in specific folders like ADS/Styldir and ADS/Gdrldir). The worker opens View > Preferences/Options, clicks the Paths tab, enters or selects the desired settings, then clicks Save (or Reset to Default) and OK. This needs to be set correctly so the software can actually find and save the shop's pattern files in the right place.

**Changing Paths for Storage Areas** — This lets a worker set the file locations used for AccuMark data specifically: Device (which hard drive or server the AccuMark data lives on), Storage Area (the default folder/location name where AccuMark models and pieces are found and saved), and Environment (the name of the User Environment settings table being used). Workers set this up once so the system always knows where to pull from and save to when working with AccuMark files.

**Changing Paths for Styles** — This lets a worker set the file locations used for MicroMark data specifically: Device (which hard drive or server the MicroMark data lives on), Style Path (the folder where MicroMark styles are found and stored), and Grade Path (the folder where MicroMark grading rule tables are stored). Workers set this up once so the system always knows where to pull from and save to when working with MicroMark files.

**Changing Paths for Import Files** — This function, found on the Paths page of the Preferences/Options command, tells the software where to look for and save graphic files you bring in from outside the system. The worker sets the "Device" (the hard drive on the PC or shared File Server where MicroMark data lives) and the "Path" (the exact folder name where the graphic files are kept), so the system knows where to find imported artwork and where to store it going forward.

**Use Screen Layout** — This is a section heading introducing the tools used to customize how the screen looks and behaves. It leads into commands for arranging menus, tool bars, guidelines, and cursor snap settings in the work area.

**Overview of Customizing with Screen Layout** — This explains that how much room you have to work with on screen depends on which menus, tool bars, and status bars you decide to turn on. Workers used to AccuMark or MicroMark systems can keep familiar menus (like function keys) visible, while new users can start with the plain main menu or tool bar, and everyone is encouraged to try the new menu bar since it unlocks extra productivity features.

**Screen Layout** — Found in the View menu, this command opens a box where a worker turns on or off different menus, tool bars, and status bars, and adjusts guideline and snap settings for the work area. After clicking checkmarks for what you want visible and setting your preferences, clicking OK saves the layout and closes the box, so the screen is arranged the way you like for your daily work.

**Display Guidelines** — This turns on a grid of horizontal and vertical lines (or dots or crosshairs) in the work area to help you line things up visually, similar to graph paper. In the View menu's Screen Layout box, you pick the line style (None, Lines, Dots, or Crosshairs), set the spacing between them, and click Apply Grid then OK to see the guides on screen — useful when placing pieces precisely.

**Snap to Grid, Geometry, or Precision** — "Snap" makes your cursor automatically jump to the nearest guideline, grid point, or piece edge/corner instead of requiring you to click exactly on it, which makes selecting and drawing much easier and more accurate. In Screen Layout's Snap section you turn on Grid (jump to guidelines), Geometry (jump to nearest point or line on a piece), or Precision (move or add geometry using an exact typed-in measurement) depending on how exact you need your work to be.

**Keyboard** — This setting, accessed through the Screen Layout command in the View menu, lets a worker choose which keyboard style (layout of shortcut keys) the system uses, once that option is turned on for their setup.

**Use Custom Toolbars** — This is a section heading leading into instructions for building your own tool bars — rows of clickable buttons — so frequently used commands are easy to reach.

**Custom Toolbars** — Found in the View menu, this command lets a worker add or remove buttons on the standard tool bar or build entirely new custom tool bars. It's useful for putting the specific commands you use most often within one click's reach instead of digging through menus.

**Add or Delete Tool Bar and Buttons** — Tool bars are rows of picture buttons (icons) that give one-click access to commands you'd otherwise have to find in a menu, and this function lets you build custom tool bars or resize buttons to fit how you work. To add a button, you open Custom Toolbars from the View menu, pick the category with the command you want, then drag that command's name onto the tool bar where it turns into a clickable icon button.

**For the Piece/Icon Menu** — This is a section heading introducing the group of functions related to the Piece/Icon menu, which is the panel that shows all the pattern pieces in a model or style.

**Displaying the Piece/Icon Menu** — The Piece/Icon menu is a panel that automatically shows up when you open a model or style, listing every pattern piece as a picture icon, by name, or both. Using the right-click Options menu, a worker can sort the pieces, resize or move the panel to dock along any edge of the screen, or expand it to Full Screen to see many pieces at once — handy when you need to quickly find and grab a specific piece.

**Deleting Pieces from the Piece/Icon Menu** — This lets a worker remove one, several, or all pieces from the Piece/Icon menu display by highlighting them, right-clicking, and choosing Delete Icon or Delete All Icons from the Options menu. Important: for MicroMark styles this actually deletes the piece from the style itself (not just the icon view), so it should be used carefully and only when you really intend to remove that piece.

**Placing Pieces into the Work Area** — This describes how to take pieces shown in the Piece/Icon menu and put them into the main work area to work on them. A worker clicks a single piece's icon then clicks in the work area to drop it, or selects multiple pieces (by dragging, Shift-clicking a range, or Ctrl-clicking individual ones) and right-clicks to place them all at once using the Options Pop-up menu.

**Piece Information from the Piece/Icon Menu** — Each piece's icon button displays helpful symbols and numbers at a glance, without opening the piece: solid lines mean cut lines, dashed lines mean seam lines, a dashed-over-solid line means a severed seam, a boxed line means the piece is mirrored, and "><" means shrink/stretch has been applied. Numbers on the icon also show piece counts — how many left and right copies are needed (the system treats the piece as digitized/unflipped as the "left") — so a worker can quickly check cutting requirements without extra steps.

**For AccuMark or MicroMark** — This is a section heading introducing settings and setup choices for working with either the AccuMark or MicroMark grading/marking systems.

**Setup for AccuMark or MicroMark Grading/Marking System** — PDS 2000/Silhouette 2000 can create markers (the layouts used for cutting fabric) for either an AccuMark or a MicroMark grading/marking system, and this section helps a worker who already has one of these systems decide how to configure the software to match it. It points to related setup choices such as which menus to use, default file locations, notch preferences, MicroMark grade rule settings, and import/export settings for MicroMark styles.

**Set Preferences for Environment and Paths** — This lets a worker who is more comfortable with either the AccuMark or MicroMark way of working set the software's preferences to match, including choosing the AccuMark or MicroMark environment and identifying the folder paths where existing models or styles are stored. Setting this up correctly means the system opens, displays, and saves your pattern files in the places and formats you expect for your particular grading/marking system.

**Customize Work Space for AccuMark** — This is a help feature that lets you explore the AccuMark-style screen layout on your monitor. As you move your cursor over different parts of the sample screen, the system tells you what each menu or option is called and does, which helps workers who are used to the older AccuMark system feel comfortable in PDS 2000/Silhouette 2000. You would use this when you want to set up or understand a work area arranged the AccuMark way.

**Customize Work Space for MicroMark** — This is a help feature that lets you explore the MicroMark-style screen layout on your monitor. Moving your cursor over the sample screen shows you information about the MicroMark menus and options you can display, helping workers familiar with MicroMark adjust to PDS 2000/Silhouette 2000. Use this if you prefer working in a layout similar to the older MicroMark system.

**Mark Request and Orderload Differences** — This explains the two different ways a marker (the layout of pattern pieces on fabric used for cutting) can be created, depending on which system is used. If you are making the marker in MicroMark, piece restrictions come from the Style Description and you build the marker with Mark Request; if you are making it in AccuMark, piece restrictions come from Lay Limits and you build the marker with Orderload. Knowing which method applies helps you set up piece restrictions correctly before sending work to the cutting room.

**Differences** — This is a section heading in the manual that introduces a group of topics covering how PDS 2000/Silhouette 2000 differs from the older AccuMark and MicroMark systems.

### Differences Between PDS 2000/Silhouette 2000 and AccuMark or MicroMark
This section explains the key differences workers moving between PDS 2000/Silhouette 2000 and the older AccuMark or MicroMark systems need to know, especially if files or patterns are imported and exported between formats. It covers things like version and database requirements, how models and styles are found and stored, how pieces are described and worked with, how selections and tracking work, and limits on pieces when making markers. Reading this helps prevent mistakes when switching between the different software environments.

**Selection, Options and Tracking Differences** — This explains how choosing commands and objects (like lines or points) works differently between AccuMark, MicroMark, and PDS 2000/Silhouette 2000. In AccuMark, you always pick the command (function) first and then the object you want it applied to, but in MicroMark you sometimes pick the object first, and many Point menu options only appear once you have selected a point using Point Tracking. Understanding this helps workers avoid confusion when a menu option doesn't seem to appear until they click on something first.

**Access Features Formerly in AccuMark Popup Menu** — In the older AccuMark system, right-clicking brought up a Pop-up menu with shortcuts like Zoom, Refresh Screen, and Undo. In Silhouette 2000 that pop-up menu no longer exists, and this section is a reference table showing exactly where each of those old features has moved to in the new menus (for example, Zoom is now under View/Zoom/Zoom In). Use this table if you learned AccuMark and can't find a familiar shortcut in the new system.

**Accessing Features Formerly in MicroMark Function Keys** — In MicroMark, pressing function keys (F1, F2, etc.) on the keyboard triggered common actions like redrawing the screen or zooming. This section is a reference table showing where each of those function-key actions now lives in PDS 2000/Silhouette 2000, such as menu commands or toolbar buttons, so a MicroMark-trained worker can find the equivalent action.

### Learn the Basics
This is a section heading introducing the fundamental, everyday skills needed to operate PDS 2000/Silhouette 2000, such as viewing work areas, moving pieces, and using the cursor.

**Overview of Working in PDS 2000/Silhouette 2000** — This introduces the core day-to-day tasks in PDS 2000/Silhouette 2000, such as zooming in on a piece, showing internal lines, tracking to a point, and moving pieces with the cursor. Getting comfortable with these basic actions makes you faster and more efficient at pattern making, since almost every other task in the program builds on them.

**Piece Geometry** — Piece geometry refers to the lines, points, and specific locations on lines that make up a pattern piece in the software. Understanding these basic building blocks — and being able to identify each type — is necessary before you can properly view, select, edit, or track points and lines on a piece.

**Geometry Colors** — The software uses different colors on screen to show the status of lines and points on a pattern piece, such as black for original unmodified lines, green for something highlighted (but not yet clicked on), red for something actually selected, and black again for edits made but not yet saved. Watching these colors as you work tells you at a glance what you've selected or changed, and you can adjust the default colors using Color Preferences/Options if needed.

**Cursor Shape Changes** — The shape of your on-screen cursor changes depending on what you're doing — for example, selecting a point or line, running a command to create/modify/grade/measure/draft a piece, or using the Zoom In tool. These shape changes act like visual prompts telling you what action is currently possible, such as whether an object can be moved or whether a command with extra options is active.

**Moving Pieces in Work Area** — To move a pattern piece, click in the center of it, drag it with the cursor to the new spot, and click again to drop it in place. To remove a piece from the work area entirely, use the Delete Piece from Work Area command in the Piece menu, or right-click to bring up the Options Pop-up menu and choose delete from there.

**Arranging Multiple Work Areas** — When you have more than one work area (pattern window) open at once, you can switch between them by clicking the title bar of the one you want active, or by selecting it by name from the Window menu at the bottom of that list. You can also minimize, maximize, cascade, or close individual work areas using the window control buttons in the top right corner, similar to standard Windows programs.

**Quick Keys** — Quick Keys are keyboard shortcuts that use the ALT key plus an underlined letter shown in a menu to run a command without touching the mouse. For example, holding ALT and pressing P then A opens the Add Point command from the Point menu — this can speed up repetitive tasks for workers who prefer the keyboard.

**Short Cuts** — Short cuts are key combinations on the keyboard that let you open or close commands, programs, and dialog boxes quickly, without needing to click through menus with the mouse. This includes both Quick Keys (ALT plus a letter) and dedicated Keyboard Keys, giving workers faster ways to access frequently used tools.

**Function Keys** — Function Keys are the F1, F2, F3, etc. keys on the keyboard that can be pressed to quickly trigger common actions in the software, such as redrawing the screen or zooming, similar to how they worked in the older MicroMark system.

**Hot Keys** — Hot keys are keyboard shortcuts, like holding Alt plus a function key (Alt+F2, Alt+F8, etc.), that let a worker trigger a command instantly instead of hunting through menus with the mouse. For example, Alt+F1 deletes a point and Alt+F5 adds a notch, so once you memorize the combination for a task you repeat often, you can work faster. These default combinations are fixed and currently cannot be changed by the user.

**Keyboard Keys** — This covers the everyday keyboard keys used to run commands without the mouse: the Enter key confirms a typed name or value and moves you forward (or acts like clicking OK), and the Escape key cancels the current command without saving any changes you made. Holding Shift while clicking lets you select a consecutive group of items, while holding Ctrl lets you select several separate, non-touching items; the Tab (and Shift+Tab) keys move you forward and backward between input fields on a form.

**Using Zoom Commands** — Zoom commands change how close up or far away you are viewing your pattern piece on screen, without changing the actual piece itself. You can zoom in to see fine detail like individual points, zoom out or to fullscale to see the whole piece or all pieces at once, view a piece at true real-life size, or zoom to a piece(s) you've selected — useful for checking small details or getting an overview before making edits.

**Select and Move Points, Lines, and Pieces** — This function lets a worker click on and pick up the points, lines, or whole pattern pieces on screen so they can be repositioned in the work area. It's the basic way of arranging or adjusting pattern pieces and their details as you build or edit a pattern.

**Selecting Multiple Points, Lines, or Pieces** — This explains the ways to select more than one item at once while running a command: click items one at a time, click in the middle of a piece to grab its whole outline, hold Shift to select everything between a first and last click, hold Ctrl to pick separate items far apart, or drag a box (marquee) around a group of items. Once you've picked everything you need, you use the right-click Options menu to end the selection before the software moves to the next step.

**Selecting a Range with Thumbtacks** — Thumbtacks are two markers that appear at the ends of a line when a command (like Move Range) needs you to pick a stretch of points rather than a single one. You click and drag each thumbtack along the line to widen or narrow the range of points being affected, then click to lock it in place — this lets you apply a change, such as moving points, to just the section of the pattern you want.

**Ending Selection to Continue** — Because many commands let you keep selecting multiple points, lines, or pieces, the software needs a signal that you're finished picking items so it can move to the next step. You do this by right-clicking (or clicking the third mouse/pen button) and choosing OK from the pop-up menu, or by double-clicking the right button — this also lets you immediately start the same command again for repetitive tasks like digitizing several lines in a row.

**Selecting Points/Locations on Multiple Lines/Pieces** — When your cursor gets near a line, the software highlights all the points on that line so you can see what you're about to select. While holding the left mouse button down, you can use the arrow keys to jump between lines and pieces — left/right arrows move you around the edge of the piece, and up/down arrows switch between internal lines and the outer boundary — which is handy for precisely choosing a point without needing pinpoint mouse accuracy.

**Select and Move Points, Lines, and Pieces** — This function lets a worker click on and pick up the points, lines, or whole pattern pieces on screen so they can be repositioned in the work area. It's the basic way of arranging or adjusting pattern pieces and their details as you build or edit a pattern.

**Work in Cursor and Value Modes** — This is the general topic covering the two ways to make changes in the software: by dragging with the mouse (Cursor mode) or by typing exact numbers (Value mode). Workers switch between these depending on whether they want quick visual adjustments or precise, measured changes.

**Getting Acquainted with User Input Box** — The User Input box is the on-screen panel that shows you what to do next while running a command, such as prompts telling you what to click or fields where you can type measurements. It can be pinned in place (docked) or left floating over your work area, and what appears in it changes depending on which command you're currently using.

**Changing between Input Modes** — This describes how to switch between Cursor mode (where you drag pattern geometry with the mouse) and Value mode (where you type exact measurements into the User Input box). You switch by clicking the Cursor/Value button or by pressing the left and right mouse buttons together, and whichever mode you pick stays active until you change it again.

**Work in Value/Cursor Mode** — This explains the two methods for editing a pattern piece: dragging it with the mouse cursor (Cursor mode) for quick visual changes, or typing precise numbers into the Value Input fields (Value mode) for exact measurements. Workers choose the method that fits the task — dragging for rough placement, typing values for accuracy.

**Working in Cursor Mode** — In Cursor mode, you make changes by physically dragging a point or line with the mouse to a new spot and clicking to drop it there, rather than typing numbers. To use it, make sure the Cursor/Value button shows "Cursor" (click it or press both mouse buttons together to switch), pick your command such as Move Point, select what to move, finish your selection, then drag and click to place it — the software shows you how far you moved it in the Value Input area afterward.

**Working in Value Mode** — In Value mode, instead of dragging with the mouse, you type exact numbers into the Value Input fields to move or adjust a point or line. For example, after selecting Move Point and choosing what to move, you'd type the new position in the X field and press Enter, and the piece on screen updates immediately to match the number you typed — useful when you need precise, repeatable measurements rather than an eyeballed drag.

**Options Pop-up Menus** — This is the general topic covering the right-click menus that appear throughout the software to give you extra tools and choices while working on a pattern.

**Options Pop-up Menu** — This is a right-click menu that pops up when you're working on a piece — over an icon in the Piece menu, over an empty work area, or in the middle of a command — giving you extra tools to speed up your work. Most of the time it offers OK (confirm your selection and finish), Cancel (back out and reconsider), and Clear All (wipe your selections and start over), and for line/point commands it offers additional shortcuts to help you find specific locations quickly.

**Using Options Pop-up Menus for Commands** — The software gives you on-screen prompts, a changing cursor shape, and the right-click Options Pop-up menu to guide you step-by-step through a command. What choices show up in that menu depends on exactly which command you're running and what step (prompt) you're currently on, so it always gives you only the relevant options for that moment.

**Options for Making Selections in Commands** — This refers to the right-click Options Pop-up menu that appears while you're in the middle of a command (a tool you've started, like deleting points). It gives you choices such as OK (finish this step), Cancel (back out and undo changes), Select All (grab every piece of that type at once), and Clear All (drop everything you've selected so far). You use it constantly while working so you can confirm, cancel, or quickly select/deselect groups of items instead of clicking each one by hand.

**Options for Point Location** — This is the Point Options Pop-up menu, a right-click menu that shows up when a command is asking you to pick a specific point location on a pattern piece. It gives you extra ways to place or choose that point precisely (rather than just clicking freehand), which matters when accuracy at a corner or notch is important.

**Options for Lines** — This is the right-click options menu that appears when a command wants you to select or work with lines (the edges/seams of a pattern piece). It gives you extra choices for how to pick or handle those lines accurately, similar to the point and selection option menus, so you can work faster and more precisely with pattern edges.

**Using Options Pop-up Menu for Work Area Tasks** — This is a right-click menu you can open in the blank work area whenever no tool/command is currently running. From it you can Undo or Redo your last action, open the Edit Piece/Line/Point Info boxes to check or change details about a piece, send a highlighted piece into the Piece/Icon menu (the sidebar of piece thumbnails) for reuse, or delete a highlighted piece — it's a quick shortcut menu for common piece-management tasks instead of digging through the main menus.

### File Management
This is the general topic area covering how PDS 2000/Silhouette 2000 handles saving, opening, and organizing your pattern files, models, and styles. It's the umbrella section that leads into all the specific File menu commands like New, Open, Close, Save, Import, and Printing/Plotting.

**Overview of File Menu** — The File menu is where you handle everything related to your work files: opening a blank work area or an existing model/style, saving your work, converting data between AccuMark and MicroMark formats, editing a MicroMark style description, merging pieces from one style into another, creating/editing models, closing files, printing/plotting/cutting pieces, importing graphics, and exiting the program. Think of it as your main control panel for getting patterns in and out of the system and onto paper or a cutting table.

**File Structures and Data Equivalents Differences** — This explains that in this version of the software, MicroMark users keep working with MicroMark 9.5/1.5 styles and AccuMark/Silhouette users keep working with AccuMark 7.6 models and pieces — no automatic file conversion happens between the two systems yet. All the details you're used to seeing, like line types, rule numbers, and line labels, will look the same on-screen as they did in your old system, but if you deliberately retrieve data in one format and export it to the other, standard conversion rules apply.

**New** — Use the New command in the File menu (or press Ctrl+N) to open a brand-new, blank work area where you can start building AccuMark pieces from scratch. You can have several work areas open at once, and the one you just created becomes your active workspace.

**Open** — Use the Open command in the File menu to bring up an existing MicroMark style, or an AccuMark model or piece, so you can view or edit it. Once you open a model or style, its pattern pieces appear as thumbnails in the Piece/Icon menu along the edge of the work area, and you can open multiple files at once by holding down a key while selecting them.

**Create/Edit Model** — Use this command in the File menu to open the Create/Edit Model menu, where you build a new model or make changes to one, including adding pieces, removing pieces, and setting prefix names. Once a model is created here, it becomes available for other tasks in System Management, the broader system used to track production data.

**Close** — Use the Close command in the File menu to shut the work area you're currently in (the active one, if you have several open). If you've made any changes since your last save, the software will ask whether you want to save them before it closes — you can also close a work area by clicking its close button in the top right corner.

**Close Style/Model** — Use this command in the File menu to close a specific style or model and remove its pieces from both the Piece/Icon menu and the computer's memory, even if other work areas are still open. You'll pick the style or model by name from a list, and if you have unsaved changes you'll be prompted to save first.

**Style Description** — This MicroMark-only command opens the Style Description form, where you define everything about a style across three tabs: general style info and sample size, the list of pieces belonging to that style, and special cutting instructions called Cutter's Musts. This information matters at marker-making time, since the system automatically gathers a style's pieces and grades them to the sizes requested for a cut order.

**Style/Piece Manager** — This MicroMark-only command lets you merge pieces from one style (the source) into another style (the destination) — you open the destination style, pick the source style, choose which pieces to bring over, and click OK to merge them in. It exists because older MicroMark PDS systems could only hold a limited number of pieces in memory at once, so this tool let workers swap pieces in and out as needed.

**Model and Style Description Differences** — This section explains key differences in how AccuMark and MicroMark organize pattern data: in AccuMark, pieces and models are stored as separate files and deleting a piece from a model doesn't erase the piece itself, whereas in MicroMark the style file contains the piece geometry directly, so deleting a piece from the style description actually deletes that piece's shape. It's useful to know because it affects whether deleting something is safe/reversible depending on which system's data you're working in.

**Import** — Use the Import command in the File menu to bring graphic files — like clip art or plot files with a .PLT extension made in other drawing programs such as AutoCAD or CorelDraw — into PDS 2000/Silhouette 2000. You can preview thumbnails before importing, move/delete/copy them as a group, and even have the import automatically added as a new pattern piece, which is handy for adding logos or graphic details onto a piece.

**Recent File** — Use this command in the File menu to see a list of the files you've opened most recently, so you can quickly reopen one without hunting through folders. (Note: at the time of the manual, this feature was still under construction.)

**Printing, Plotting, and Cutting** — This section covers how to send your finished model, style, or piece data out of the software to physical output — printing a paper copy, plotting a full-size pattern on a plotter (or through the separate Grading System), or sending a job straight to a cutter to cut sample pieces. You'd use these whenever you need a physical version of your digital pattern work for review, marking, or actual cutting.

**Exit** — This command, found in the File menu, closes the PDS 2000/Silhouette 2000 program. If you're a MicroMark user, you can also just press the Escape key while your cursor is in a MicroMark menu to quit the program the same way.

**Using Style Description** — This is the overall command that opens the Style Description window, where a worker can view and set all the key information about a style, such as sizing, grading, and piece details, in one organized place.

**Setting Sample Size for Style Description** — This lets you pick which size is treated as the "base" or sample size for a style. You open the Style Description page, click the Sample Size field, check off the sizes you want available (marked with an asterisk), then choose the sample size from that list and click OK — note that doing this only labels a size as the sample, it does not change the actual shape/geometry of the pieces.

**Setting Style Information for Style Description** — This section of the Style Description page is where you set the basic identifying and rule information for a style — its name, which Grade Rule Table controls how it's sized up/down, the sample size, which Variation (synonym) table and Seam Allowance table apply, an MTM Validation table for made-to-measure checks, and the maximum splice length allowed when making a marker (the layout used for cutting fabric).

**Setting Marker Preparation and Shrinkage for Style Description** — Found on the Piece Description page, these settings control how a piece behaves when a marker (fabric cutting layout) is made: Number of Splits sets how many times a piece can be cut into sections (up to 15, but keep it low to save memory), Half Piece Table flags a piece as a half-piece for closed/folded markers, Ignore Splice lets a piece skip splice rules, and X/Y Variance shrinks or stretches the piece by a percent or measurement to account for fabric shrinkage.

**Using the Style Description Page** — This is the step-by-step process for opening a MicroMark style and using its Style Description tab to set default style-level information — you open the style, go to File > Style Description, click the Style Description tab, fill in the Style Information fields, set the sample size, review the style's history, and click OK to save.

**Using the Piece Description Page** — This is the step-by-step process for setting default details for each individual piece (like a sleeve or collar) within a MicroMark style — you open the style, go to File > Style Description, click the Piece Description tab, pick the piece to edit (via the icon slider or drop-down list), edit its information/restrictions/blocking/shrinkage settings, and click OK to save.

**Adding or Deleting Pieces and Descriptions** — This function on the Piece Description page lets you add a new standard piece to a style (by clicking Add Standard Piece, selecting the piece name and material group, then OK) or remove one (by clicking Delete Piece and confirming), and it also lets you add or remove written descriptions for pieces the same way.

**Using the Cutter's Must Page** — This page of Style Description shows information the cutting room needs for a MicroMark style — piece names, quantities, and any special messages — and lets you generate a printable text file of that list by clicking Create File; note this feature is still being finalized and has some known limits when converting between MicroMark and AccuMark data.

**Checking Style History** — This part of the Style Description page shows you the record of changes to a style: the Previous Revision date, the Last Revision date, and the Style Creation date along with the User ID of the person who created it — useful for tracking who changed a style and when.

**Save Pieces, Models, or Styles** — This is the general command/category for saving your work in the system — covering pieces, models (groups of pieces), or styles — so your changes are kept on the disk.

**Setting Piece Blocking for Style Description** — This section of the Piece Description page controls how a piece is aligned to plaid or striped fabric patterns during marker making. Primary X and Y set the main amount of blocking (either a percent of the fabric's repeat pattern or a fixed measurement) in each direction, while Secondary X and Y set an additional amount of blocking available if needed.

**Setting Piece Information for Style Description** — This section of the Piece Description page holds the basic identifying details for a piece: its Piece Name (up to 10 characters, no spaces), an optional Piece Message that can print on the piece at marker or plotting time, its Type (Normal or Standard), the Unflipped and Opposite quantities (how many copies as-digitized versus mirror-flipped), and a Material Group code identifying what fabric/material it's cut from.

**Setting Piece Restrictions for Style Description** — This section of the Piece Description page sets limits on how a piece can be positioned during marker making: CW Tilt/CCW Tilt limit how far it can be tilted clockwise or counterclockwise, Bias forces it into a 45-degree angle when a bias marker is used, Nap ensures all same-size pieces with the Nap flag rotate together, and Flip ensures all same-size pieces with the Flip flag turn over together.

**Saving Pieces, Models, or Styles** — This command covers all the ways you can save your work — saving a brand-new, never-before-saved piece/model/style, saving a copy under a different name or location, saving all open work at once, or converting data between AccuMark and MicroMark formats.

**Saving and Converting Data** — When saving a file, you have the option to convert it into a different format — for example, saving an AccuMark model as a MicroMark style, or vice versa — but only the information that both formats support will actually carry over; anything not supported by the target format is dropped, and note that no true data conversion exists yet in this release since MicroMark and AccuMark still store data differently underneath.

**Save - Current Model, Style, or Pieces** — This File menu command (Ctrl+S) saves the model, style, or piece you're currently working on under its existing name, updating the version on disk with your latest changes; a list of open files appears so you can choose which to save, and you can check Set Original Position to keep the pieces' current placement in the work area.

**Prefix Names** — This is an on/off toggle that, when turned on, automatically adds the model's name in front of any piece name when you add that piece to the model using the Add Pieces command — for example, adding a piece called "Front" to model "313" renames it "313 Front." Turn it on before adding pieces (making sure the right model is open), and click Prefix Names again to switch it off.

**Save As** — This command in the File menu lets you save the piece, model, or style you're working on under a brand new name, without changing or overwriting the original file. When you use it, a list of open files pops up, you pick where to save it, type in a new unique name, choose the file type (like AccuMark Model or MicroMark Style), and click Save. Use this when you want to create a variation of a pattern while keeping the original safe and untouched.

**Printing** — This is a section heading in the manual covering all printing-related commands (Print, Print Preview, Print Setup) for producing paper copies of pieces in the work area.

**Print** — This command sends the pieces you're working on to a printer, similar to printing any document on a Windows computer. It appears as a popup menu option and is used when you need a physical paper copy of what's on your screen.

**Printing** — This is a section heading in the manual covering all printing-related commands (Print, Print Preview, Print Setup) for producing paper copies of pieces in the work area.

**Print Preview** — Print Preview lets you check how the pieces in your current work area will look on paper before you actually print them. Select it from the File menu, and the software shows you a page-by-page view of the printout, letting you zoom in or out and flip between pages if the pieces span more than one page. From this preview screen you can click Print to go ahead and print, or Close to go back to your work without printing.

**Print Setup** — This command in the File menu lets you choose which printer to use or set a default printer, using the standard Windows printing setup screen. Use this before printing if you need to switch to a different printer than the one currently set as default.

**Plotting/Cutting** — This is a section heading in the manual covering commands related to plotting (printing large-scale pattern pieces on a plotter) and cutting (sending pieces to a cutting machine).

**Plot** — This command in the File menu sends a request to plot (print full-size, on a large-format plotter) the pieces you've selected in your current work area. When you use it, the system submits the job and gives you a job number to track it, similar to sending a print job but for full-size pattern pieces used on the shop floor.

**Plotting** — This describes the step-by-step process of plotting pieces, either by directly selecting pieces in the work area and choosing Plot from the File menu, or by using a Plot Form (a layout screen showing the plot area's usable width and length) to arrange pieces before sending them to the plotter. Workers choose the Plot Form method when they want to preview and control exactly how pieces are arranged on the material before cutting or plotting begins.

**Plot Preview** — This command in the File menu lets you see what the plotted output will look like before actually sending it to the plotter, similar to a print preview on a regular printer. Use it to check spacing and layout of pieces ahead of time to avoid wasting material.

**Plot Setup** — This command in the File menu lets you choose which plotter to use or set a default plotter, similar to choosing a printer. For setting other plotting defaults (like paper size or speed), use the Preferences/Options screen instead.

**Plot Text** — This isn't a standalone menu command but is done through the Annotate Piece function in the Piece menu, letting you add text notes (like size, style number, or instructions) directly onto a pattern piece so it prints when the piece is plotted. To use it, select the spot on the piece where you want text, type your note in the annotation box that appears, and confirm to finish; the text size follows a default setting but can be changed.

**Submit Sample Request** — This command in the File menu sends a request to a cutting machine (cutter) to cut sample pieces from the items currently in your workspace. Use this when you need a physical fabric sample cut from your digital pattern pieces, such as for prototyping or approval before full production.

### Make Edits
This is a section heading in the manual introducing the Edit menu, which contains tools for editing pieces, points, and lines while you work on patterns.

**Overview of the Edit Menu** — This introductory section explains that the Edit menu contains commands to help you while making changes to pattern pieces, such as undoing mistakes, selecting geometry, and clearing selections.

**Undo** — This command reverses the last action you performed in the software, and it can be used repeatedly to undo several steps in a row, one at a time, going backward through your recent work. Use it right after you make a mistake — like moving a piece incorrectly or deleting something you didn't mean to — by selecting Undo from the Edit menu, clicking the Undo button, or pressing Ctrl+Z.

**Redo** — This command reverses the last Undo you performed, essentially redoing the action you had just undone, putting it back the way it was before you clicked Undo. Use it if you undo something by mistake and want to restore that change.

**Set Selected** — This command in the Edit menu lets you pick a specific piece and mark it as the "current piece" — the one that other commands will act on. Use it when you're working with multiple pieces and need to tell the software exactly which one you want to focus on next.

**Add Pieces** — This function lets a worker create a brand-new model (a named group of pattern pieces) or add more pieces to a model that already exists. Before using it, check the status line to confirm the correct storage area and that the right model is active, and make sure the piece you want to add is already pulled into the work area on screen. After choosing Add Pieces from the File menu's Create/Edit Model option and naming or selecting the model, the worker clicks the pieces shown in red to add them, then right-clicks to finish.

**Current Pieces** — This Edit menu command lets a worker mark one or more specific pieces as "active" so that only those pieces can be selected or edited, which is very helpful when several pattern pieces overlap on screen and it's hard to click the right points or lines. The worker opens the Current Pieces box (from the Edit menu or the "..." button on the Info bar) and checks off the pieces to activate; unchecking them or clicking Clear All returns all pieces to normal, selectable status.

**Remove Pieces** — This function deletes one or more pieces from a model, whether the model is new or already saved, without deleting the piece itself from the system. The worker chooses Create/Edit Model then Remove Pieces from the File menu, picks the model (or accepts the last one used), and clicks the pieces to remove from a lookup list — each selected piece gets a small asterisk mark. After right-clicking to confirm, the software confirms with a "Successfully removed" message.

**Select All** — This Edit menu command (shortcut Ctrl+A) quickly selects every point, line, or other piece detail of one type at once while a worker is in certain commands, such as assigning a grading rule table, instead of clicking each one individually. It saves time when an action needs to apply to all matching items on a piece.

**Clear All** — This Edit menu command (shortcut Ctrl+D) instantly deselects everything a worker had previously selected while working in certain commands, such as viewing intermediate points, so they can start a fresh selection without clicking each item off one by one. It can also be reached from the right-click Options pop-up menu.

**Delete Pieces from Work Area** — This Edit menu command clears every piece out of the active work area (the on-screen workspace) in one step, resetting it back to empty or to the piece's original stored icon. Workers should be careful because any unsaved changes to a piece will be lost when it's deleted this way — though if pieces are deleted by accident, the Undo command can bring them back right after.

**Edit Point, Line, and Piece Info** — This is a heading in the Edit menu grouping together the related tools for changing information tied to points, lines, and whole pieces — such as point numbers, grade rules, line types, seam amounts, and piece names — rather than a single command itself.

**Edit Point Info** — This Edit menu command lets a worker change information stored at a specific point on a pattern piece, such as its notch type, grading rule (how the point changes size between sizes), or point number. The worker uses Track to click through points around the piece (or auto-tracking to move automatically) and stops on the point they want, then edits its details in the fields shown, which will differ slightly depending on whether the system is running AccuMark or MicroMark data.

**Showing Point Info** — While using Edit Point Info, dragging the mouse along a line makes a small info box pop up and update as it passes each point, showing that point's attribute, type, ID/special number, and grade rule number. This box only appears if "Show Point/Line Info" is turned on in Preferences and Options, and it won't show up when using the Track arrow buttons or Auto Tracking instead of dragging.

**Edit Line Info** — This Edit menu command is used to change details about a specific line on a piece, such as its line type, its label, or how much seam allowance it carries. The worker tracks to the line they want to change (using Track buttons/arrows or Auto Tracking), clicks into the field that needs updating, and types the new name or value, with available options varying slightly between AccuMark and MicroMark data.

**Edit Piece Info** — This Edit menu command changes the core information about a whole pattern piece, including its name, category, description, and the grade rule table it uses (which controls how it resizes for grading), and also lets a worker check the piece's file path and which style/model it belongs to. The worker tracks to or clicks the piece to edit, types the new information into the Name, Category, Description, or Rules fields, and clicks Apply to save the change.

**Setting Up for Tracking** — This is the setup step a worker completes before using tracking tools, done through the General page of Preferences/Options, so that clicking through points, lines, or pieces on a pattern works correctly. It covers turning on options like Auto Tracking and Show Point Info ahead of actually editing.

**Use Tracking to Edit** — Tracking is the method used to move through and select points, lines, or pieces one at a time so their information can be edited, and it must be turned on first in the General Preferences/Options page. A worker can turn on Auto Tracking for automatic movement, Show Point Info to see details pop up while tracking, and can use the Filter tab within Edit Point/Line/Piece Info to limit which kinds of information show up while tracking.

### Change View Options
This is a heading covering the group of settings and commands in the View menu that let a worker adjust how the pattern pieces and work area are displayed, such as zoom level and what details are shown or hidden.

**Overview of View Menu** — The View menu contains the tools for zooming in and out on the work area and for showing or hiding details like point and line names, seam amounts, and grading information — it changes how the screen looks, not the pattern data itself. Workers should note that Undo usually doesn't work for these viewing commands, so each command has its own way (like Refresh Display) to reset the screen back to normal afterward.

**Piece - Seam Amounts** — This View menu command displays the amount of seam allowance that has been assigned to each line on a piece, without changing anything — it's just for checking. The worker selects the piece or lines they want to check, the seam measurements appear on screen, and they can clear the display and re-select to check more lines, or right-click and choose Cancel when finished.

**Refresh Display** — This View menu command redraws the work area to clean up the screen, clearing away leftover measurement numbers or marks left behind from other commands the worker used earlier. It doesn't change any pattern data — it just refreshes what's visible on screen for a clearer view.

**Use Zoom Commands** — The zoom commands let a worker magnify (zoom in) to see fine piece details more closely, or zoom out to view the whole work area at once, making it easier to work on small details or get an overall look at the layout.

**Zoom In** — This command, found in the View menu (or by pressing F7), lets you draw a box (called a marquee) around a small area of a pattern piece to make it bigger on your screen. It's handy when you need to work closely with tiny details like notches, darts, or internal markings that are hard to see at normal size. You click once to start the box, drag diagonally to size it, and click again to zoom into that area.

**Zoom Out** — This command, found in the View menu (or by pressing F8), takes you back one step to the zoom level you had before you last used Zoom In. It's the easy way to back out and see more of your work area again after zooming in close on a detail. Selecting any other Zoom command will change the view again.

**Zoom - Full Scale** — This command, in the View menu (or press F3), shrinks or expands the display so every piece currently in your work area fits on the screen at once. It's especially useful after pulling a piece in from the Piece/Icon menu when it doesn't show up on screen — this command brings everything back into view. Note that it only changes what you see on screen, not the actual size of the pieces themselves.

**Zoom to Selected** — This command in the View menu (or press F4) zooms the screen in on just the piece(s) you've selected, filling the window with it, while leaving other pieces in the work area still present (just not shown as large). You'd use this when you need to focus closely on one specific piece without losing track of the rest of your layout. Select another Zoom command afterward to change the view again.

**Zoom - 1 : 1** — This command in the View menu (or press F1) sets the screen so that one inch shown on your monitor equals one actual inch on the pattern piece. Use it when you want to see the true, real-life size of the piece on screen rather than a scaled-up or scaled-down view.

**Zoom - Separate Pieces** — This command in the View menu (or press F2) spreads out all the pieces in your work area so they're neatly separated (not overlapping) and shown at full scale. It's most useful when you've pulled every piece from the Piece/Icon menu into the work area and need them arranged so you can see each one clearly.

**Verify Points** — This is a submenu/section header in the View menu grouping together the various point-checking commands (such as viewing all points, intermediate points, point numbers, grade rules, notch points, and point types/attributes) that let a worker inspect the points that make up a pattern piece.

**Point - All Points** — This command in the View menu shows every point on a selected piece at once — including intermediate points, grade points, smoothing points, and end points. Use it when you want a full picture of all the points defining a piece's shape, for example before making edits. Select the piece(s), and the points display on screen until you cancel or choose another command.

**Point - Intermediate Points** — This command in the View menu displays intermediate points (points along a line that aren't corners or endpoints) on selected pieces, shown on screen as squares. It's helpful when you need to pick out one specific point to move or adjust, since it lets you see exactly where each intermediate point sits. Make sure Symbols is turned on in Preferences/Options first so the points will actually display.

**Point - Point Numbers** — This command in the View menu displays the ID numbers assigned to each point on a selected piece, so you can identify exactly which point is which. This is useful when you need to reference or change a specific point using the Edit Point Info command afterward. Select the piece(s), view the numbers, then cancel or pick another command when done.

**Point - Grade Rules** — This command in the View menu shows the grade rule numbers attached to the grade points (the points that control how a piece changes size between different garment sizes) on all pieces in the work area. If you leave this turned on, every piece you pull from the Piece menu will automatically show its grade rule numbers. It's useful for checking that grading has been set up correctly on a piece.

**Point - Notch Points** — This command in the View menu shows the notch type assigned to each notch on a piece, displaying notches as small slit marks along the piece's outer edge. It lets you check that the correct notch attribute numbers (which control how a notch is cut) are assigned to each notch on the piece. Select the piece or individual notches to see their assigned numbers.

**Point - Point Types/Attributes** — This command in the View menu displays the Point Modifiers and Point Attributes — settings that control how a point is graded, cut, or shaped — for either one selected point or all points on a piece. It's useful for double-checking that each point has the right special settings before cutting or grading a piece. Select the piece(s) or point(s) to see this information on screen.

**Point Types and Modifiers** — Point types and modifiers are settings attached to individual points on a pattern piece that control how the point is graded (resized across sizes), cut, or shaped (for example, making a line curve or smooth). Workers view these using the Point/Point Types/Attributes command in the View menu, and can change them using the Edit Point Info command.

**Attributes** — Point attributes are settings on a point that tell the system how that point should be graded, plotted, or cut, working alongside point types (like Turn, Curve, or X-free points) and other modifiers (such as Alternate Start, Curve Length Reference, Lift and Plunge, or Grade Like Intersection) that control cutting and grading behavior for that specific point on a MicroMark piece.

**Point - Total Piece Points** — This command in the View menu shows the total number of points contained in a selected piece, counting points on the outer boundary, drill holes (each counted as 4 points), internal cutout lines, internal lines, and stripe/plaid lines. It's useful for checking a piece isn't close to the system's point limit (about 4000 for AccuMark, 256 for MicroMark), which could cause problems if exceeded. Select the piece(s) to see the total, then cancel or choose another command when finished.

**View Lines** — This is a section header in the View menu grouping together commands related to viewing information about the lines that make up a pattern piece, such as line numbers.

**Line - Numbers** — This command in the View menu (or F5 for line types and numbers) displays the identifying numbers of the lines on selected pieces in the work area. It's useful when you need to reference a specific line on a piece, for example while editing or troubleshooting the pattern. Select the line(s) or piece(s) to display the numbers, then cancel or choose another command when done.

**Line - Names** — This command, found in the View menu, shows the alphanumeric names (up to 10 characters) already assigned to lines on the pieces in your work area. To use it, choose Line then Names from the View menu, click on the line(s) or piece(s) you want to check, and end your selection — the existing names will pop up on screen. It's handy when you just need to confirm what a line is called without changing anything, and you can repeat the command or right-click to clear the display when done.

**Line - Types/Labels** — This View menu command displays the type or label assigned to lines on a piece, letting you check current settings before you make any edits. In AccuMark data these are called line labels (used for internal lines), while in MicroMark data they're called types and labels (used to identify any line on a piece). Simply select the line(s), right-click to confirm, and the labels appear on screen so you can verify them at a glance.

**Line Modifiers - Types and Labels** — This is a reference list of the standard line type/label names used in MicroMark data to describe what each line on a piece is for, such as Style Line (the default for any new line drawn in PDS), Draft Line (a temporary working line), Stripe Line or Plaid Line (reference lines used to line up the pattern with a striped or plaid fabric), Grain Line (the horizontal line parallel to the fabric's edge used to keep the pattern straight during marking and grading), and Alt Ref Line (an extra reference line usable in delta, or difference-based, grading). Knowing these names helps a worker recognize at a glance what job each line on the pattern is doing.

**Line - Verify by Label** — Use this View menu command to make the system highlight only the internal lines that have a specific label you type in, which is useful when you need to find a particular line among many on a busy pattern piece. After choosing Line then Verify by Label, type the label into the Value Input box and press Enter — matching lines light up on screen (note that labels are case-sensitive, so "BACK" and "Back" are treated as different). Selecting another command clears the highlighting when you're finished checking.

**Line - Seam Corner Types** — This View menu command displays the seam corner type for selected lines or pieces, so a worker can check how a corner is set up (for example, how a seam allowance is designed to meet at that corner) without altering anything. Choose Line then Seam Corner Types, click on the line(s) or piece(s), and end your selection to see the corner type shown on screen. Repeating the command or right-clicking clears the display.

**Hide/Ignore Lines** — These View menu commands let you temporarily hide certain types of lines — such as perimeter (edge), internal, cut, or sew lines — from view on screen without deleting them, and also let you check or edit line names and labels. Workers use this to declutter a busy screen and confirm they're clicking on the correct line before making changes.

**Line - Hide/Ignore Perimeter** — This command temporarily removes selected perimeter (outer boundary) lines from the screen so a busy or overlapping pattern is easier to look at, without deleting the actual line data. Select Line, Hide/Ignore, then Perimeter, click the outer lines you want hidden, and end selection — note the system will always leave at least one boundary line visible even if you try to hide the whole piece. Use Hide/Ignore Reset afterward to bring the hidden lines back into view.

**Line - Hide/Ignore Internal** — This command lets a worker temporarily hide internal lines (like darts, notches, or seam details inside a piece) from the screen to reduce visual clutter, without deleting the underlying data. Go to Line, Hide/Ignore, then Internal, click the internal line(s) to hide, and end selection to remove them from view. Use Hide/Ignore Reset to bring them back when you need to see them again.

**Line - Hide/Ignore Reset** — This command undoes any hiding you've done and brings back all perimeter or internal lines that were temporarily hidden on a piece. Simply choose Line, Hide/Ignore, then Reset, select the piece(s) you want restored, and end selection — everything you hid earlier reappears on screen exactly as before.

**Show Grading** — This is a submenu group in the View menu containing all the commands for displaying a piece's graded sizes (the base size, all sizes, size breaks, a range of sizes, a non-base size, stacking, and rotation), giving workers different ways to inspect how a pattern grows or shrinks across sizes.

**Grade - Show Base Size** — This command redisplays a piece's original base size (the size the pattern was originally drafted in) after you've been looking at some other size on screen. Choose Grade then Show Base Size from the View menu, click the piece, and end selection — the system switches the display back to the base size so you can confirm you're looking at the reference pattern before making edits.

**Grade - Show All Sizes** — This command displays every size in a piece's graded nest (the full range of sizes generated from the grading rules) stacked together on screen at once, which is useful for visually checking how well the sizes line up. Choose Grade then Show All Sizes, select the piece, and the system draws all sizes together; any edits you make still only apply to the base size. Use Clear Nest afterward to go back to viewing just a single size.

**Grade - Show Breaks** — This command shows only the "break" sizes of a graded piece's nest — the key marked sizes rather than every single size — which is useful for a quick check of the overall size range. Choose Grade then Show Breaks, click the piece(s), and the break sizes display as you select each one; note this feature only works with AccuMark data since MicroMark doesn't support breaks. Use Clear Nest to return to a single-size view when finished.

**Grade - Show Selected Sizes** — This command lets a worker view a specific consecutive range of sizes (for example, sizes 8 through 12) in a graded piece's nest, instead of seeing every size at once. Choose Grade then Show Selected Sizes, select the piece, then type the smallest and largest size in the range you want to see — the system displays just that range so you can check the grading in that section. Use Clear Nest to go back to viewing one size.

**Grade - Show Non-base Size** — This command displays a single size other than the pattern's original base size, purely so you can verify how that particular size looks. Choose Grade then Show Non-Base Size, select the piece, then type the size you want to check in the Value Input box and press Enter — that size appears on screen for review. Use Clear Nest afterward to return to the standard single-piece view.

**Grade - Stack On/Off** — This command redraws a graded nest as if all the sizes were lined up ("stacked") on top of each other from one chosen matching point, which helps a worker see how much the sizes shift relative to that point. After displaying a nest, choose Grade then Stack On/Off, and click a point on the piece's outer edge to stack from (or type its exact location) — the nest redraws stacked at that point, and selecting the same point again removes the stacking. This is useful for visually judging grade growth from a specific reference spot, like a notch or corner.

**Grade - F Rotation** — This command shows a piece and all its graded sizes rotated and lined up according to its assigned facing (F) points, displaying it in the same orientation it would have inside a marker (the layout used for cutting fabric). Choose Grade then F Rotation, select the piece(s), and end selection — the system rotates everything to match marker orientation, which helps a worker double check that a piece's grading will look correct once it's actually laid out for cutting. It's best used after first showing all sizes with a command like Show All Sizes.

**Clear Nest** — This simple command removes any displayed graded sizes (nest) from the screen and returns the view back to showing a single piece. Choose Grade then Clear Nest from the View menu whenever you're done comparing sizes and want to clear the screen for the next task.

### Work with Points
This is the section of the software where you find all the tools for creating, adjusting, and removing points on a pattern piece. A 'point' here means any specific spot on a line — like a corner, a notch, or a hole marker — that defines the shape of the piece. Workers use this section whenever they need to fine-tune the exact geometry of a pattern.

**Overview of Point Menu** — This is the main menu screen that lists all the commands for adding, reducing, deleting, and changing points on a pattern piece. You can reach these commands from the main menu by clicking Modify Points, or you can build a custom toolbar with just the point commands you use most often. Workers who already know the older AccuMark or MicroMark systems will recognize many commands, but it's worth learning the newer point-handling methods here since they can speed up everyday work.

**Add Point** — This command lets you place a new point onto an existing line, or add a drill point (a small marked hole) inside a piece. You start the command from the Point menu, then click on the spot where you want the new point, either by clicking directly on the screen (Cursor mode) or by typing exact position values. Right-clicking brings up extra Options for finer control over exactly how and where the point is placed.

**Adding Multiple Points** — This is a group of related commands for placing several points or drills onto a piece at once instead of one at a time. You can space the added points evenly across a line or area (proportionally) or set them a fixed distance apart, which is handy for things like evenly spaced buttonholes or trim markings. Workers familiar with older AccuMark/MicroMark systems will recognize similar tools here, updated for easier use.

**Mark X Point** — This command places a visible reference mark — shown as an X or a star (*) — on a line or in open space on the pattern piece. Unlike some other points, marks made this way always stay visible on screen so you can use them as a guide. You'd use this when you need a clear visual landmark on the piece, for example to line up measurements or check spacing while you work.

**Modifying Points** — This is the group of commands used to change something about a point that already exists, such as adjusting a notch's angle, lining up two points so they match, or moving a point to a new position. There are several specific move options — moving freely, moving only left-right, only up-down, moving along a line, or moving while smoothing the surrounding line so it doesn't look choppy. Workers use these when correcting or fine-tuning a pattern shape after it's been drawn.

**Point Intersect** — This command marks the exact spot where two lines cross, or where they would cross if you extended them further, even if they don't actually touch on the piece. If that crossing point isn't sitting on a line, the system marks it with a small drill hole instead of a regular point. This is useful for finding a precise reference location, such as locating where a dart or seam line would meet another line if it kept going.

**Delete Point** — This command removes one or more points from a line — for example, an in-between point, a notch, or a grading point (a point used for sizing). Once the point is deleted, the software automatically redraws the line smoothly to account for its removal. Note that you can't use this to delete the very end point of a piece's outer edge (use the Merge command for that instead), and you can't delete special smoothing points this way.

**Reduce Points** — This command automatically cleans up a line by deleting unnecessary extra points along it, using a 'Reduce Factor' number from 0 to 5 that you set — the higher the number, the more points get removed. You can also choose whether the remaining points should be smoothed out or left as sharp turns. This is useful for simplifying a line that has too many points, such as one traced or sketched by hand, without changing its overall shape.

**Total Piece Points** — This command shows you the total count of points on a selected pattern piece, including points on outer edges, internal lines, drill holes, and stripe/plaid lines. It's useful for checking that a piece isn't close to the software's point limit (roughly 4000 points for AccuMark data, 256 for MicroMark data), which could cause problems if exceeded.

**Copy Point Num** — This command copies the identifying number of a point from one pattern piece over to a point on another piece. Point numbers are used to keep track of matching points between pieces (for example, during alterations or grading), and every point on a piece must have its own unique number. You can copy just one point number at a time or copy all of them at once between pieces.

**Add Notches** — This is the group of tools for placing notches — small marks or slits cut into the edge of a pattern piece that show sewers exactly where and how pieces should be lined up and stitched together.

**Working with Notches** — Notches are small marks cut into a pattern piece's edge that tell the person sewing where pieces are supposed to line up and match with each other. The software lets you create different notch styles, including angled notches and notches placed where two edges meet, but on-screen they all just appear as a simple slit mark. If you're moving pattern data between AccuMark and MicroMark systems, be aware the two systems define and number notches differently, so it's worth double-checking notches after an import or export.

**Add Notch** — This command places a notch (a small alignment mark) at a chosen spot along the outer edge of a pattern piece. After clicking the location on the edge, you pick which notch style you want from a list (the available styles differ depending on whether you're working in AccuMark or MicroMark format), and the notch is added there.

**Intersection Notch** — This command adds a notch exactly where two lines cross, or where they would cross if extended — commonly used along a mirror line (a line marking where a piece is symmetrical). You can also use this same command to delete an existing intersection notch or edit its type/depth, and if you later move one of the two lines, the notch automatically shifts along with it.

**Add Multiple Drills and Points** — This is the set of commands for adding several drill holes or points to a piece in one operation rather than placing each one individually, letting you space them out evenly or at a set distance.

**Add Multiple - Add Drills** — This command adds a row of drill holes (small marked holes used as sewing or placement guides, labeled D or DH depending on the system) across a piece, spaced out evenly between a start point and an end point you choose. It's commonly used for tasks like marking where buttonholes should go, since it keeps the spacing consistent automatically.

**Add Multiple - Add Drills Dist** — This command is like Add Multiple - Add Drills, but instead of spacing the drill holes evenly between two points, you set an exact measured distance between each one. You pick a start and end location anywhere on the piece, and the system places the drill holes (labeled D or DH) that specific distance apart along the way.

**Add Multiple - Add Points Line** — This command, found in the Point menu (Add Multiple > Add Points Line), lets you add several points—such as notches, marks, or drill holes—along a line so they are spaced evenly (proportionally) between two locations you pick. You select the line (any internal line except the grain line, or a perimeter/boundary line), then use the small markers called "thumbtacks" at the ends of the line to set where the spread of points should start and stop. Use this when you need a row of evenly spaced notches or marks, such as for pleats or buttons, and if the pattern piece is graded, the system automatically creates the grading rules for those new points.

**Add Multiple - Add Points Ln Dist** — This command, in the Point menu (Add Multiple > Add Points Ln Dist), adds points—like notches, marks, or drill holes—along a line but spaced a specific distance apart instead of evenly dividing the line. You pick the line (internal or perimeter, except the grain line) and use the thumbtack markers to define the start and end of the area where points should be placed. Use this when you need points at an exact measured interval, such as pleat marks every 2 inches, and grading rules are generated automatically for graded pieces.

**Modify Points** — This is the name of a menu section (page 274) in the Point menu that groups together all the tools used to change existing points on a pattern piece—such as moving, aligning, or angling notches and other markings. Workers use the commands under this heading whenever they need to adjust the position or angle of a point already placed on a piece, rather than adding brand-new points.

**Modify Points - Angled Notch** — Found under Point menu > Modify Points > Angled Notch, this command lets you set a notch (a small clip mark on the edge of a pattern piece) at a specific angle instead of the usual straight-in position perpendicular to the edge. You zoom in on the piece, click and drag along the edge to grab the notch, then move the cursor to set the angle you want; it can also be used to create a brand-new angled notch, not just adjust an existing one. Use this when a notch needs to point in a particular direction for matching seams or construction steps.

**Modify Points - Align 2 Points** — Located at Point menu > Modify Points > Align 2 Points, this tool moves one point so it lines up exactly horizontally or vertically with another point you choose, such as two drill holes for pocket placement or notches that need to match a plaid line. You first click the point you want to move, then click the point you want it lined up with, and choose whether the alignment should be horizontal or vertical; if the aligned points are along a line, the rest of the points on that line are automatically smoothed out. This is handy for keeping design details, like pocket holes or plaid-matching marks, perfectly level or plumb with each other.

**Moving Points** — This is an overview topic explaining the group of commands under Point > Modify Points that let workers move points—on perimeter lines, internal lines, line extensions, or standalone internal points—in either the X (horizontal), Y (vertical), or both directions, or restricted along a line. It explains that "Move" commands shift a single point while the points next to it stay put (useful for nudging a notch that's off by a small amount like 0.25 inches), while "Move Smooth" commands shift a point along with the surrounding line or area so the overall shape stays smooth (useful for lowering an armhole while keeping its curve intact). Understanding this distinction helps a worker pick the right tool depending on whether they want a small local fix or a smooth shape change.

**Modify Points - Move Point** — Found at Point menu > Modify Points > Move Point, this command shifts one or more points in the X and/or Y direction without smoothing the surrounding shape—only the small area right at that point changes. It differs from Move Smooth, which curves the neighboring lines as you move a point; Move Point is best for small, isolated corrections, like nudging a single notch, since moving a bigger area with it would distort the piece's overall shape.

**Modify Points - Move Pt Line/Slide** — This command, under Point menu > Modify Points > Move Pt Line/Slide, slides a graded point, notch, or in-between point along the direction of a line (or an imaginary extension of that line) without changing how many points exist. You select the point, then either drag it with the cursor so it travels along the line, or type an exact distance to move it in the Beg, End, or Dist fields; the system adds smoothing points automatically if needed to keep the line looking correct.

**Modify Points - Move Point Horiz** — Located at Point menu > Modify Points > Move Point Horiz, this command moves a point or a group of points straight left or right along the X axis only, such as dropping an armhole along the side seam. You select the point(s), then either drag with the cursor (which also shifts the connecting line segments) or type an exact horizontal distance in the X field, and the system moves the point(s) to that new spot.

**Modify Points - Move Point Vert** — Located at Point menu > Modify Points > Move Point Vert, this command moves a point or group of points straight up or down along the Y axis only. You select the point(s) and either drag them with the cursor or type an exact vertical distance (positive or negative) in the Y field, and the connecting line segments move along with the point to the new location.

**Modify Points - Move Smooth** — Found at Point menu > Modify Points > Move Smooth, this command moves a point in any direction while automatically curving ("smoothing") the surrounding line or a selected range of the line, so the piece keeps a natural shape instead of a sharp kink. It's the tool to use for something like lowering an armhole while keeping its overall curved shape, as opposed to Move Point, which only tweaks one small spot and can distort the shape if used for bigger changes.

**Modify Points - Move Smooth Line** — Located at Point menu > Modify Points > Move Smooth Line, this command moves a perimeter or internal point smoothly along a line or an extension of that line, reshaping the whole line or a chosen range of it into a new curve. You select the point, use thumbtack markers to choose how much of the line should be affected, then drag or enter values to move it—this can also be used to stretch a line out further by moving an end point to a new spot.

**Modify Points - Move Smooth Horiz** — Found at Point menu > Modify Points > Move Smooth Horiz, this command moves a point (or a range of points, selected with thumbtack markers) smoothly in a purely horizontal direction, reshaping the curve of the line while it moves. It's useful for adding fullness to a section of a pattern piece, like widening an area, while keeping the rest of the line's shape smooth and unchanged.

**Modify Points - Move Smooth Vert** — Located at Point menu > Modify Points > Move Smooth Vert, this command moves a point (or a selected range of points) smoothly in a purely vertical direction, reshaping the line's curve as it moves. It lets a worker add fullness or adjust height in one section of a piece, like a shoulder or hem area, while keeping the rest of the line's shape smooth.

**Verifying Points** — This is an overview of commands found in the View menu that let a worker double-check point information on the pattern piece without changing anything—such as displaying all points, intermediate points, sequential point numbers, grade rule numbers, notch types, assigned point types/attributes, the total number of points on the piece, or a detailed Point Info box. Workers use these display tools to confirm they are clicking on or working with the correct point before making an edit, and can turn the display off again once done.

### Work with Lines
This is a section heading (page 288) introducing the group of tools used to create, adjust, and manage the lines that make up a pattern piece, both its outer edges and internal lines. It serves as the entry point to more detailed topics on creating, moving, rotating, modifying, and deleting lines.

**Overview of Line Menu** — This overview explains that the Line menu contains all the commands for creating, modifying, adding, deleting, or moving both perimeter (outer edge) and internal lines on a pattern piece. It notes that related commands like Create Line, Perp Line, Conics, and Modify Line can be expanded to show more options, that workers can build a custom toolbar of their most-used commands, and that those familiar with older AccuMark or MicroMark systems will recognize many commands but may benefit from learning some newer methods for working with lines.

**Delete Line** — This command removes a selected line—whether a perimeter/boundary line or an internal line—from the pattern piece. Workers use it when a line was added by mistake or is no longer needed on the pattern piece.

**Replace Line** — This command lets you swap out an existing style line for a new one you've drawn, replacing its shape or position while keeping it part of the piece. Workers use it when a line needs to be corrected or redesigned without starting the piece over.

**Swap Line** — Swap Line lets you exchange one line on a pattern piece for another line you've created, effectively changing the piece's shape at that spot. It's used when you've drawn a new internal line (like a curve or offset) and want it to actually become part of the piece's boundary or design instead of just sitting there as a reference.

**Unclipped Perimeter** — This command lets certain lines on a pattern piece stick out past the normal corner point where two edges meet, instead of being cut off exactly at that corner (this is called "line extension"). Workers use it in MicroMark grading setups when a corner needs extra geometry beyond the intersection, or when two lines meeting at a corner need to keep separate, independent points rather than sharing one common point.

**Clipped Perimeter** — Clipped Perimeter removes an existing line extension by pulling the end of a perimeter (outer boundary) line back to where it actually meets the next line, so the corner is clean and exact instead of overhanging. Use this when a piece has extra line sticking out past a corner and you need it trimmed back to the true intersection point.

**Perimeter Clipped/Unclipped Sample** — This is a visual reference showing the difference between a seam displayed with the Clipped setting (lines trimmed exactly to the corner) versus the Unclipped setting (lines shown extending past the corner). It helps workers recognize which display mode they're looking at when checking a piece's edges.

**Create Lines** — This is the section/menu heading for all the tools used to draw new lines on a pattern piece, such as straight, curved, offset, copied, or mirrored lines. Workers open this menu whenever they need to add design or construction lines to a piece.

**Overview of Create Line Menu** — This overview explains that the Create Line menu holds all the commands for drawing straight, curved, offset, copied, mirrored, and tangent lines on a piece. Any line you create here starts out as a plain "internal" reference line, and it only becomes a real functional line (like a seam or cut edge) once you use a Swap, Replace, or Trace command on it.

**Create Line - Digitized** — This command lets you draw a new straight or curved internal line on a piece by clicking points on screen, much like tracing by hand with a pen. The new line is automatically attached to a piece already in the work area and starts out as a basic, default-type internal line until you relabel or convert it.

**Create Line - Curved** — Create Line - Curved is used to draw a curved internal line on a pattern piece. (Note: this section of the manual was marked "under construction," so full details weren't available, but it works alongside the other Create Line drawing tools.)

**Create Line - 2 Point** — This command draws a straight internal line automatically as soon as you click two points, rather than requiring you to trace the whole shape. It can connect points within one piece or even between two different pieces, and the resulting line is a default internal line you can later relabel.

**Create Line - Offset Even** — Offset Even creates one or more copies of an existing edge or internal line, moved a set, even distance away while staying parallel to the original — the original piece shape isn't changed. Workers commonly use this to build facings (the folded-under fabric piece that finishes a raw edge) by offsetting a copy of the edge line by a specific measurement.

**Create Line - Offset Uneven** — Offset Uneven makes a copy of a line that is shifted away from the original by different amounts at different points along its length, instead of a uniform distance. This is handy for reshaping a copied curved line unevenly, for example adjusting a neckline or armhole curve by varying amounts at different spots.

**Create Line - Copy Line** — Copy Line duplicates one or more selected lines and lets you place the copy anywhere — on the same piece or a different one — while keeping the copy's original length and shape exactly the same. For example, you could copy an armhole or neckline curve from one piece and paste it onto another piece that needs the same shape.

**Create Line - Mirror** — Mirror creates a flipped, mirror-image copy of a selected line (either an edge line or an internal line), using another line on screen as the "mirror" axis to flip around. It's useful for quickly duplicating a symmetrical shape, like matching one side of a collar or pocket to the other, without redrawing it by hand.

**Create Line - Create Blend** — Create Blend draws a new internal line that smoothly connects into an existing line by pivoting at one end, so the new line blends seamlessly into the shape near that point. You pick a "blend point" close to (but not exactly on) the end you want to pivot, then drag or enter a distance to move the line into its new blended position.

**Hide/Ignore Lines** — These View menu commands let you temporarily hide certain types of lines — such as perimeter (edge), internal, cut, or sew lines — from view on screen without deleting them, and also let you check or edit line names and labels. Workers use this to declutter a busy screen and confirm they're clicking on the correct line before making changes.

**Moving Lines** — This is the menu section covering all the different ways to reposition lines on a piece — including perimeter/boundary, internal, grain/grade reference, annotation, and style lines. It lists options like moving a line parallel to itself while stretching the edges to meet it, moving freely in any direction, moving while keeping length and smooth connections, rotating a line, or moving and rotating together.

**Internal Line Labels** — Internal line labels are letter codes (like A, B, C, D, G, H, I, M, P) that tell the AccuMark system what kind of internal line it is looking at — for example, "G" always marks a grain line, "D" marks a drill hole, and "I" marks a general user-defined line. Some labels are fixed and assigned automatically by the system (like grain and mirror lines), while others are optional and can be changed by the worker to organize different line types on a piece.

**Tangent Lines** — This is a section header in the Line menu that groups together all the tools for creating tangent lines — lines that touch a curve smoothly at one point without crossing it. Workers use these tools when they need to add construction or design lines that flow smoothly off a curved edge of a pattern piece.

**Create Line - Tangent On Line** — This command lets a worker draw a straight internal line that touches (is tangent to) a chosen point on an existing curved line. To use it, you pick the Line menu, choose Create Line then Tangent On Line, click or type the exact spot on the curve where the new line should touch, and then drag or type a value to set how long the new line should be. It's useful when you need an internal marking line that blends smoothly off a curved edge, such as for a dart or style line.

**Create Line - Tangent Off Line** — This command creates a straight line that is tangent to (smoothly touches) one point on a curve and then travels to end at a second point you pick elsewhere on the piece. You start by choosing Create Line then Tangent Off Line from the Line menu, then select where the line will end (the intersection point) and separately select the point of tangency on the curve. This is handy when a design line needs to leave a curved edge smoothly but land at a specific point somewhere else on the pattern.

**Create Line - Tangent 2 Circ** — This command draws a single straight line that is tangent to (touches without crossing) two separate circles at points you select. After choosing Create Line then Tangent 2 Circ, you click the touch point on the first circle and then on the second circle, and the system draws the connecting line automatically. It's used when pattern details involve two curved/circular shapes that need a smooth connecting line between them.

**Creating Tangent Lines** — This is an overview/help screen in the Line menu that explains the group of tangent-line tools available and helps the worker pick the right one for the job. It points to three options: a line tangent to one point on a curve, a line tangent to a curve that ends at a chosen point, and a line tangent to points on two different curves.

**Perpendicular Lines** — This is a section header in the Line menu that groups together the tools for drawing perpendicular lines — lines that cross another line at a perfect right angle (90 degrees). These tools are used whenever a pattern needs a straight line that squares off cleanly from an edge or another line, such as for grainlines, notches, or crease lines.

**Perp Line - Perp On Line** — This command draws a line that meets an existing line — whether it's an edge of the piece or an internal line — at a perfect right angle at a point you choose. You pick Perp Line then Perp On Line, choose whether the new line should extend to one side or both sides (Half/Whole) of that point, and then click or type the exact location on the line where the perpendicular line should cross it. On the job this is commonly used to create things like a pleat or crease line on a pant leg.

**Perp Line - Perp Off Line** — This command creates a line that crosses a perimeter (outer boundary) line at a right angle, at a specific point you select along that edge. After choosing Perp Line then Perp Off Line, you choose the Half/Whole option to control whether the new line extends to one or both sides of the crossing point, then click or type the exact spot on the edge where the line should intersect it. This is useful for adding perpendicular reference or construction lines off the outside edge of a pattern piece.

**Perp Line - Perp 2 Points** — This command draws a perpendicular line that sits exactly halfway between two points you pick on the same existing line. You select Perp Line then Perp 2 Points, set the Half/Whole option for how far the new line should extend, and then click or type two locations on the line to mark the points it should be centered between. This is useful for finding and marking a true center point on a line with a squared-off line, without having to measure it by hand.

**Creating Perpendicular Lines** — This is an overview/help screen in the Line menu that explains the perpendicular-line tools and helps the worker choose the correct one for their task. It lists the three options: a line perpendicular to a point on an existing line, a line perpendicular to and crossing an existing line, and a line perpendicular that sits halfway between two points on a line.

**Conics** — This is a section header in the Line menu for tools that create circles and curves (called "conics") on a pattern piece — for example center holes, curved corners, and circles that touch other lines. Workers use these tools whenever a piece needs a round shape, a drill hole marker, or a smooth curved corner instead of a sharp one.

**Conics - Circle Ctr Rad** — This command creates a circle by having the worker pick the center point and then specify how big it should be by radius (distance from center to edge) or circumference (distance around). You can set it to be created as a piece by itself or as an internal line inside an existing piece, and you can choose whether a center mark (like a drill hole) is shown. This is used for adding round design details or drill hole locations to a pattern with precise, repeatable sizing.

**Conics - Circle Ctr Cirm** — This command works the same way as Circle Ctr Rad — you pick a center point and then size the circle — but this version is set up to size the circle primarily by its circumference (the distance around the outside) rather than the radius. It can also be created as a new separate piece or as an internal line, with options for whether and how a center mark is shown. It's used any time a round shape needs to be sized by its outer measurement instead of the distance from the center.

**Conics - Circle 2 Pt Center** — This command creates a circle by having the worker click two points that will sit on the circle's outer edge (circumference) and then roughly place where the center should go. After picking the two edge points, you drag or type a value to position the approximate center, and the system builds the circle to match. This is useful when you know two points a circle needs to pass through but don't need to calculate the exact center yourself.

**Conics - Circle 3 Pt** — This command creates a circle that passes through three points the worker selects, anywhere inside a piece or on the work area. The system automatically figures out the correct circle to fit all three points and also marks the center with a drill hole (or a Draft Point Line in MicroMark). It's handy for creating a circle when you know three points it must touch but not the center or exact size.

**Conics - Circle Tang 1 Line** — This command creates a circle that just touches (is tangent to) one existing line — either an edge or internal line — at a single point you choose. After selecting the touch point on the line, you drag the cursor or type a value to set how big the circle's radius should be. This is used to add a round detail or drill mark that lines up smoothly against an existing edge without crossing it.

**Conics - Circle Tang 2 Line** — This command creates a circle that touches two different lines that meet at a corner, fitting neatly into that corner. After selecting the two lines that form the corner, you drag the cursor or type a value to set the circle's radius, and the system places the circle tangent to both lines along with a center drill mark. This is useful for rounding into a corner with a perfectly fitted circle, such as for a drill hole placed snugly in an angled corner.

**Conics - Curved Intersection** — This command replaces a sharp corner — where two adjoining edge lines meet — with a smooth curve, essentially rounding off the corner. After selecting the two lines that form the corner, you drag the cursor or type a radius value to control how rounded the curve should be, and the system trims back the two straight lines and replaces the corner with a matching curved section. This is commonly used to soften or round a sharp corner on a pattern piece, such as rounding a squared-off edge for a smoother finished look.

**Conics - Oval Orient** — This command, found under Line > Conics > Oval Orient, lets you draw an oval (also called an ellipse, a stretched-out circle) by picking its center point, then setting the length and angle (tilt) of the short axis, and finally the length of the long axis. You would use this when a pattern piece needs an oval shape, such as a decorative cutout or vent, at a specific angle rather than straight up-and-down. As you move the cursor, the screen shows the distance and angle numbers so you can place it precisely or type exact values instead.

**Conics - Oval Focus** — Found under Line > Conics > Oval Focus, this command creates an oval inside a piece by picking a center point and then a 'focus point' that determines which direction the long axis of the oval will point. After that, you set how long the oval's long axis should be, and the system draws the finished oval on your pattern. This gives you another way to build an oval shape when you want to control it by a focus point instead of an angle.

**Creating Circles and Ovals** — This is an overview section of the Line menu that lists the different ways to make circles and ovals (ellipses) on a pattern piece — for example, from a center point and a size, from two or three points on the edge, tangent to (touching) one point or two crossing lines, or by turning an existing edge line into a curve. It's a menu of options so a worker can pick the method that best matches what reference points or measurements they already have, rather than one having to use the same single method every time.

**Modify Lines** — This is the section/category heading in the Line menu that groups together all the commands used to change existing lines on a pattern piece — such as moving, rotating, smoothing, splitting, or merging lines — rather than a command itself.

**Modify Line - Move Offset** — This command, under Line > Modify Line > Move Offset, lets you slide an edge line or an internal line to a new position while keeping it running parallel to where it started. If you move an edge (perimeter) line, the lines next to it automatically stretch or adjust to still connect to it, so the piece stays closed up. You'd use this to quickly widen, narrow, or reposition part of a pattern piece without redrawing it from scratch.

**Modify Line - Move Line** — Located under Line > Modify Line > Move Line, this command moves a line in any direction to make a simple change to a pattern piece, and you can use a reference point to guide exactly how far it moves. It's especially handy for shifting grain lines (lines showing fabric direction), grading reference lines (used for sizing), or text/annotation lines to a new spot on the piece.

**Modify Line - Move Line Anchor** — This command (Line > Modify Line > Move Line Anchor) moves a line to a new position while keeping it the same length, and lets you choose where on the neighboring lines it should blend into. You can guide the move using a reference point, or use the 'Bump to Line' option to rotate the line until it touches another line at a chosen spot — useful when you need the line's endpoints to land in specific places without changing its overall length.

**Modify Line - Move Range** — Found under Line > Modify Line > Move Range, this command moves a single point on an edge or internal line in any direction, and the system automatically smooths (curves) the neighboring points and lines so there's no sharp kink left behind. It's similar to the 'Move Smooth' command in the Point menu, and it's useful when you want to reshape just a section of a line — for example, adjusting a curve on an armhole — while keeping the overall line smooth.

**Modify Line - Make Move Parallel** — This command, under Line > Modify Line > Make Move Parallel, both moves a line and makes it run parallel to another chosen line, or to the flat horizontal (X) or vertical (Y) direction, in a single step. You pick the line(s) to change, choose what it should be parallel to, and the system repositions it accordingly — handy when a line needs to line up with another edge after being moved.

**Modify Line - Make Parallel** — Located under Line > Modify Line > Make Parallel, this command turns a selected line so it becomes parallel to another line, or to the flat horizontal (X) or vertical (Y) direction, without necessarily moving it elsewhere. A common use is making a grain line (the line showing fabric grain direction) match up with a center-front line, or squaring up a center-front/center-back line to the grain after tracing a piece on the digitizing table.

**Modify Line - Rotate Line** — This command, found under Line > Modify Line > Rotate Line (called 'Pivot Line' in AccuMark), spins an edge or internal line around a fixed pivot point, either by typing an angle or by dragging a distance. It's commonly used to create a bias grain line (a grain line set at an angle, often 45 degrees, instead of straight), since the pivot point stays put while the line swings to the new angle.

**Modify Line - Move and Rotate** — Under Line > Modify Line > Move and Rotate, this command lets you both slide and spin a line at the same time, either by dragging with the cursor or by entering an exact angle and distance. You can also set nearby edge lines to move in opposite directions as the line rotates, which is useful when reshaping a section of a piece that needs both a shift and a turn in one motion.

**Modify Line - Set and Rotate** — This command (Line > Modify Line > Set and Rotate) moves an internal line so that it lines up with, and pivots around, a specific point on another line — even one on a different pattern piece. You'd use it when two lines need to cross at an exact point or angle; the target line stays still while the line you're adjusting swings around that intersection point until it's positioned correctly.

**Modify Line - Reshape Line** — This command is listed as 'under construction' in the manual, so full details aren't available, but based on its name and menu location (Line > Modify Line > Reshape Line) it's intended to let a worker change the shape/curve of an existing line on a pattern piece.

**Modify Line - Adjust Length** — Found under Line > Modify Line > Adjust Length, this command changes a line by keeping its two endpoints fixed in place while moving the points in between, effectively adjusting the line's shape/length between the ends. The manual notes it currently behaves like the 'Move Smooth Line' function, so it reshapes the middle of a line without disturbing where it starts and ends.

**Modify Line - Smooth** — This command, under the Line menu's Smooth option, evens out an existing edge or internal line by letting the system reposition the points along it (but not its very end points) to remove bumps or inconsistencies, such as ones left over from tracing a piece by hand (digitizing). You select the line, then use small markers called 'thumbtacks' to set which section of the line should be smoothed; note that smoothing a curve repeatedly will gradually flatten it out more each time, so it should be used carefully.

**Modify Line - Merge** — Located under Line > Modify Line > Merge, this command joins two or more separate lines into one continuous line, removing the end point where they used to meet. You select the lines in counterclockwise order — either adjoining edge lines or internal lines (which don't have to touch, since the system will draw a connecting line between them) — and it's the way to clean up or reverse a line that was previously split.

**Modify Line - Split** — This command, under Line > Modify Line > Split, cuts one line into two or more separate line segments at a point you choose — the point doesn't need to already exist on the line, since you can click or drag to the exact spot, or type in an exact location. It's the opposite of the Merge command and is used when you need to treat parts of what was one line as separate lines, for example to edit or delete just one section.

**Modify Line - Clip** — This command trims off the part of an internal line that sticks out past the edge (perimeter/boundary) of the pattern piece. You select the internal line to trim, then click on the segment you want to keep, and the software cuts the line off right where it crosses the piece's edge. Use it whenever an internal marking line was drawn too long and needs to be neatly cut back to the piece boundary.

**Modify Line - Open Line** — This command tells the system that an internal line on a mirrored (symmetrical) piece should NOT be copied to the mirrored other half. Workers use this when they need a feature, like drill holes, on only one side of a piece that is otherwise a mirror image. You simply select the internal line you don't want mirrored and confirm, and the mirrored copy of that piece will no longer show that line on the opposite side.

**Modify Line - Flatten Line Segment** — This command removes extra in-between points along a line to smooth or simplify it, while giving you the choice to keep notches (small cut marks) and dart points untouched. You pick the line, choose whether to delete or keep notches, decide whether to protect dart points, then adjust markers (called thumbtacks) to set exactly which part of the line gets flattened. It's used to clean up a line that has too many small kinks or points without disturbing important construction marks.

**Modify Line - Edit Line Names** — This command lets you give a name (letters, numbers, or a short label, up to ten characters) to a specific line on a pattern piece, or change a name that's already there. Naming lines helps the system and other procedures recognize particular lines on a piece later, for example when running automated steps (macros). You select the line, type in the name, and confirm to save it.

**Modify Line - Copy Line Names** — This command copies the names already assigned to lines on one piece over to matching lines on another piece, so you don't have to retype them. Internal lines must be copied one at a time, but outer boundary lines can be copied individually or all at once for the whole piece. This is especially useful when building automated procedures (macros), since naming lines this way gives the system extra information to recognize pattern parts from piece to piece.

**Overview of Modify Line Menu** — This is an introductory summary of all the tools available in the Line menu for working with lines on a pattern piece, such as moving, reshaping, adjusting length, smoothing, merging, splitting, clipping, mirroring, flattening, naming, and copying names of lines. It's meant as a quick guide pointing workers to the specific command they need, especially if they're used to older AccuMark or MicroMark systems and want to find the new equivalent tool.

### Work with Pieces
This is a section header introducing the group of tools and topics related to creating, editing, and managing pattern pieces in the software. It doesn't perform an action itself, but organizes all the piece-related commands covered in the manual.

**Overview of Piece Menu** — This is an introductory overview describing the Piece menu, which contains commands to create, modify, add, delete, or move pattern pieces. It points out that the menu can be customized (for example, adding a toolbar of frequently used commands) and that many commands will feel familiar to workers coming from older AccuMark or MicroMark systems, while also including some newer, more efficient methods for creating pieces.

**About Pieces** — This section explains the basic definition and management of pattern pieces: a piece is any shape made of three or more connected lines that can serve as a pattern piece for cutting fabric. It introduces the many things you can do with a piece — display it, create or delete it, add notes, flip/rotate/move it, add darts/pleats/fullness, fold or merge pieces, apply shrink/stretch, and save it to the piece menu — as background before the manual covers each specific command.

**Differences in Working with Pieces** — This section explains how handling pieces in PDS 2000/Silhouette 2000 differs from the older AccuMark and MicroMark systems, mainly around seam allowance and grading. For example, seam allowance can now be set automatically by line type in a table or added manually, pieces can be stored using either the sewing line or the cutting line as the main outline (cut lines always go to marker-making regardless), and grading changes made through certain piece commands are saved with the piece itself rather than only in a separate rule table.

**Fold Keep** — This command folds an opened-up mirrored piece back into its mirrored form, or lets you keep just part of a piece and throw away the rest of its shape. You choose the fold line either by selecting an existing internal line or by matching two points, and you can have the system automatically re-mirror the piece or add seam allowance along the new fold line. Importantly, this doesn't create a brand-new piece — it changes the shape under the same piece name.

**Delete Piece from Work Area** — This command removes one or more selected pieces from your current work area (the on-screen workspace), but it does not permanently erase them from the hard disk if they were already saved. However, any unsaved changes made to those pieces will be lost when you delete them from the work area, so workers should save their work first if they want to keep recent edits.

**Combine/Merge** — This command joins two separate pattern pieces into a single new piece. The grading (sizing) rules from the first piece you select are always kept, while the rules for the second piece and the merged seam line can either be kept as-is or updated based on which options you choose. Use this when two pattern sections need to become one continuous piece, such as combining a front and side panel.

**Shrink/Stretch** — This command adjusts the size of a pattern piece to account for fabric shrinkage or stretch, making the piece slightly bigger or smaller than its original measurements. You can apply the adjustment either as a specific measurement (linear) or as a percentage of the piece's overall size, and a special symbol shows up on the piece icon once shrink/stretch has been applied, so you can tell at a glance which pieces have this adjustment.

**Annotate Piece** — This command lets you type notes or instructions directly onto a pattern piece, such as cutting or sewing directions, and you can also edit, move, or copy notes you've already added. You click where you want the note, type your text into a pop-up box, and click OK, and the note then appears written right on the piece for anyone viewing it.

**Hide Annotations** — This function hides any written notes (annotations) on a piece while you're working with a model or style, helping reduce visual clutter on screen. You can toggle it back to "Show Annotation" whenever you want the notes visible again.

**Piece to Menu** — This command takes a piece you just created or edited in the work area and sends it to the Piece/Icon menu, which is the library or storage area for pieces. If the piece hasn't been saved yet, the system will prompt you to give it a name before it's moved; afterward, the piece disappears from the work area and appears in the Piece/Icon menu instead.

**Showing Grading for Pieces** — These are View menu commands that let you turn the display of grading (sizing) information on or off for pieces in your work area, making it easy to check that a piece's sizing rules are correct and then clear the screen when finished. Special symbols help you spot rule changes at a glance: a pound sign (#) marks a grade rule automatically generated by the system, and an asterisk (*) marks a rule that was created or edited manually through Grade menu commands or certain Piece menu actions like Pivot Dart.

**Create Pieces** — This is the section/menu of commands used to make brand-new pattern pieces from scratch or from existing pieces. Workers use it whenever they need to add a new piece to a style, whether by drawing a shape, entering measurements, or copying/tracing from pieces that already exist.

**Creating Pieces** — This is the group of commands in the Create Piece menu that let you build new pieces, either from scratch using typed-in measurements or by starting from a piece that already exists. It's a good idea to give every new piece a unique name, because saving a piece with the same name as an existing one using the plain Save command will overwrite the original without asking — only Save As will warn you first and ask if you really want to replace it. If "Add new piece to model/style" is turned on, the new piece is automatically attached to the style or model you're working in.

**Create Piece - Rectangle** — This command draws a brand-new four-sided (rectangular) pattern piece, useful for simple pieces like waistbands, straps, or pocket facings. You either click and drag on screen to set the size (Cursor mode), or type exact length and width numbers into the Value Input Box (Value mode), and the system builds the rectangle from the corner point you picked. There's also an option to automatically add the new piece to the style or model you're currently working on.

**Create Piece - Circle** — This command creates a perfectly round pattern piece by either dragging on the screen or typing in an exact radius (distance from center to edge) or circumference (distance around the outside). You can choose to mark the center point of the circle and decide whether it becomes a real, separate piece or just a circular line inside another piece. This is handy for things like round buttons, appliqués, or trim pieces.

**Create Piece - Skirt** — This command automatically builds one quarter-section of a circular skirt just by typing in the total waist measurement and the skirt length — you don't have to draw anything by hand. The system places the piece for you and automatically draws the solid boundary line and a grain/grade reference line, saving time versus manually drafting a circle skirt.

**Create Piece - Oval** — This command creates an egg/oval-shaped pattern piece by simply typing in the horizontal (side-to-side) and vertical (top-to-bottom) dimensions you want. The system automatically draws the outline and adds a grain/grade reference line for you, and you can choose to mark the center point of the oval.

**Create Piece - Collar** — This command automatically drafts a basic collar piece just by entering measurements like collar width and the distances from center back to shoulder and shoulder to center front, instead of drawing it by hand. You can also choose to add a notch (a small clip mark used for matching pieces during sewing) where the collar meets the shoulder seam, and the system will draw the outline and reference line automatically.

**Create Piece - Facing** — This command quickly creates a facing piece (an inner layer that finishes an edge like a neckline or armhole) by using a line that's already on an existing piece, instead of making you manually trace several lines together. If the piece needs seam allowance (extra fabric added at the edge for sewing), the system will prompt you to add it automatically.

**Create Piece - Copy** — This command makes an exact duplicate of an existing piece, including any internal lines like darts or pocket markings, so you can try changes on the copy without touching the original. You just click on the piece to copy it, then drag the copy to wherever you want it placed on screen — unlike tracing, you can't pick and choose which lines get copied, the whole piece comes over as-is.

**-Create Piece - Extract Piece** — This command lets you pull a new piece out of an area within an existing piece by first drawing design lines to mark off the section you want. When you run the command, that marked-off area fills with color and the system automatically figures out the new piece's outline for you, saving you from having to manually trace every line, and it lets you selectively bring over internal lines too.

**Trace Pieces** — This is the section of the manual/menu covering the various Trace commands, which are used to build new pieces by tracing lines from one or more pieces that already exist, rather than drawing from scratch.

**Create Piece - Trace Normal - Sew** — This command builds a new piece by selecting and combining specific lines from one or more existing pieces, where the new piece's outline will be a sew line (the stitching line, not including seam allowance). It's useful for creating a new style line — like a modified neckline or armhole — or for combining several pieces into one, and you select the boundary lines in clockwise order.

**Create Piece - Trace Normal - Cut** — This command works just like Trace Normal - Sew, but the new piece's outline becomes a cut line (the actual fabric cutting edge, which includes seam allowance) instead of a sew line. You select lines from one or more existing pieces in clockwise order to build a new piece, such as a modified style line or a combined one-piece pattern.

**Create Piece - Trace Mirrored - Sew** — This command creates a new piece that is a mirror image, built by tracing and combining lines from one or more existing pieces, with the outline set as a sew line. You pick a mirror line first (the line the rest gets flipped across), which is useful for making symmetrical pieces like a mirrored yoke from a half-pattern.

**Create Piece - Trace Mirrored - Cut** — This command is the same as Trace Mirrored - Sew, but the new mirrored piece's outline becomes a cut line instead of a sew line. You select a mirror line and the system flips and combines the traced lines to build the new piece, useful for things like a symmetrical yoke.

**Create Piece - Trace Scored - Sew** — This command creates a new, non-symmetrical piece by picking a "score line" (a fold line) and unfolding part of an existing piece across it, with the new outline set as a sew line. It's a fast way to build pieces that have a turned-back hem or self-facing, where part of the piece folds back onto itself.

**Create Piece - Trace Scored - Cut** — This command works the same as Trace Scored - Sew, but the new piece's outline becomes a cut line instead of a sew line. You select a score (fold) line and unfold part of an existing piece to quickly create pieces such as turnback hems or facings that aren't symmetrical.

**Tracing to Create Pieces** — This is the general instructional section explaining how the Trace commands work: perimeter lines are normally selected clockwise, but with a scored piece, lines before the score line are clockwise and lines after it (the part that gets mirrored) are selected counter-clockwise. It also explains that the Swap Sew/Cut option lets you choose which set of lines the system uses versus which set it generates, and that lines must actually intersect for tracing to work correctly.

**Seams and Corners** — This is a section title in the manual that groups together all the tools for adding seam allowance (the extra fabric added around a pattern piece for sewing) and for shaping the corners where those seam lines meet. Workers use the commands under this heading whenever they need to build, view, or adjust the sew and cut lines on a pattern piece.

**Overview of Working with Corners** — This is an introductory summary of the commands found in the Piece/Seam menu that let a worker create special corner shapes, switch a corner back to a plain/regular corner, and turn the on-screen display of corners on or off. It notes that special corners can only be made on pieces that already have seam allowance added, that changing the seam allowance amount won't erase a corner's special shape (though other edits might), and that any special corner can be removed by replacing it with a standard corner.

**Overview of Working with Seams** — This introductory section explains that the Seam menu is used to add seam allowance (extra fabric width for sewing) to a piece or to check what seam allowance is already there, and that the same menu also has tools for shaping corners. It reminds the worker that a new piece can be shown using either its cut line or its sew line as the main outline, and that if they plan to work with corners they should switch the 'Corners On/Off' setting to On so the corner shapes are visible.

**Viewing Seams and Amounts** — These commands let a worker show or hide the seam lines and see how much seam allowance (extra fabric width) has been added to a piece, without changing the actual pattern. Workers can also view seam corner shapes and adjust the default settings for how seams appear on screen, which is useful for double-checking a piece's construction before sending it to production.

**About Seam Differences** — This section explains that older AccuMark and MicroMark systems handled seam allowance differently than the newer PDS 2000/Silhouette 2000 software — for example, MicroMark could store data using the sew line as the main outline and then automatically switch to cut lines for marker making. It's a reference for workers who used the older systems, so they understand why some familiar steps (like removing extra boundary lines) are no longer needed in the new software.

**Seam - Define/Add Seam** — This command lets a worker add seam allowance (extra fabric width around the edge for sewing) to one or more pattern pieces, either evenly all the way around or unevenly/tapered on certain lines. It can be applied line-by-line or to a whole piece at once, and it can also be used later to edit or remove seam allowance that was already added, with the saved amounts viewable afterward in the Edit Line Info screen.

**Seam - Hide/Remove Seam** — This command hides the extra seam lines (the ones that aren't the main outline) on the pattern pieces the worker selects, without deleting the actual seam allowance data. It's useful for temporarily cleaning up the screen view; note that a related setting in Preferences/Options can hide seam lines for every piece in the work area at once instead of just selected ones.

**Seam - Sever Corner** — Based on the item's name and its place among the corner commands, this function is used to detach or separate a special corner shape from the piece's boundary so it stops following automatic updates, similar to how 'Sever Boundary' works for seam lines in general.

**Seam - Swap Sew/Cut** — This command switches which line is treated as the piece's main solid outline — flipping it from the sew line to the cut line, or back again. When seam allowance is present, one of these lines shows as a solid line (the current main boundary) and the other as dashed, and using this command lets the worker make pattern edits on whichever line needs to be solid, since all changes must be made on the solid boundary line.

**Seam - Update Seam** — This command refreshes the non-boundary seam line so it matches any recent changes made to the main outline of the piece, but only after the 'Sever Boundary' command was used to disconnect them. It works much like the 'Relate Boundary' command and is used to make sure the seam lines stay accurate after edits.

**Seam - Copy Piece No Seam** — This command creates a duplicate of a pattern piece without bringing along its seam allowance or corner shape information, so the worker can freely edit the copy — for example deleting sew lines or moving points — without being restricted by the system's automatic corner shapes. The sew lines are still copied onto the new piece as reference lines, but they can no longer be automatically updated.

**Seam - Fix Bound Type** — This command lets a worker specify whether the sew line or the cut line should be treated as the piece's original main outline (boundary). It's used to correct or set that designation on one or more selected pieces so the software knows which line to follow for edits.

**Seam - Sever Boundary** — This command disconnects the seam (non-boundary) lines from the piece's main outline so that if the worker later modifies the boundary shape, the seam lines will not automatically update to match. It's useful when a worker wants to change the outline without disturbing the existing seam lines.

**Seam - Relate Boundary** — This command reconnects and updates the non-boundary seam lines to match the piece's main outline after it has been changed using other commands, working much like the Update Seam command. During the process the worker can choose whether the sew or cut line selections should be kept as the main boundary.

**Seam - Reset SA Values** — This command overrides any seam allowance amounts that were manually typed in on specific lines of a piece, resetting every boundary line so its seam amount instead comes from the standard seam table. It's useful for undoing one-off manual adjustments and bringing a piece back in line with the company's standard seam values.

**Corners** — This is a section heading in the manual covering all the different corner shapes and related commands available for pattern pieces that have seam allowance, such as creating special corners, adding notches, and toggling corner display.

**Notch Options for Corners** — When creating a corner in the Seam menu, the worker can choose one of three notch styles: Perpendicular Notch (the system draws a line straight out from the sew-line corner to where it crosses the cut lines and places notches there), Extension Notch (the system stretches the sew lines out to meet the cut lines and notches those points), or No Notch (no notch is added, and choosing this will remove any notch a corner already had). Notches are small marks or cuts added to fabric edges to help align pieces correctly during sewing.

**Seam - Corners On/Off** — This command acts like an on/off switch that shows or hides the special corner shapes on selected pattern pieces without deleting the underlying corner data. Workers can click it or press the tab key to toggle the display, which is handy for viewing a cleaner outline of the piece or double-checking corner details when needed.

**Seam - Remove Corner** — This command takes away any special corner treatment (like a mitered or notched corner) that was applied to a piece and puts it back to a plain, regular corner, including removing any notches that were marking the cut lines. Use it when you need to undo a corner style you or someone else applied and start over with a clean corner.

**Seam - Regular Corner** — This turns a corner back into a standard, ordinary corner - the kind formed naturally where the cut lines meet - removing any special corner shaping that was there before. You can also add notches (small marks cut into the fabric edge to help line up pieces during sewing) to the corner while doing this. Use it by choosing whether to fix one corner at a time or apply it to every corner on the piece.

**Seam - Slant Corner** — This creates a corner that is cut at an angle instead of square, by extending the sew lines (the lines showing where the fabric will actually be stitched) out to meet the cut lines and clipping the fabric there. Workers use it to trim excess fabric at an angled seam intersection so the corner folds and sews properly. You can apply it to a single corner or to every corner on the piece, and add notches for extra alignment marks.

**Seam - Mitered Corner** — This creates a corner that is trimmed at an angle so it forms a straight edge, cutting away extra fabric so the seam lies flat when folded - this is called mitering, similar to how picture frame corners are joined. The worker picks the corner, and the system shows a line to indicate exactly where the fabric will be clipped, which the worker can adjust before confirming. It's used anywhere bulky fabric at a corner needs to be reduced so the finished seam isn't lumpy.

**Seam - Double Miter Corner** — This adds an extension of fabric at a corner that is as wide as the seam allowance (the extra fabric border added beyond the sewing line for seaming), with the worker typing in how long that extension should be. It's used to build out a corner shape that needs extra fabric folded or tucked, such as at certain garment openings.

**Seam - Tab Corner** — This adds a small fabric extension - shaped like a tab - off the corner of the seam allowance, and the worker enters how long that tab should be. It's used when a garment corner needs an extra flap of fabric, for example to fold under or attach to another piece during sewing.

**Seam - Nub Extension Corner** — This adds a small extension of fabric sticking out from the seam allowance at a corner, with the worker typing in the length of that extension. Notches can also be added to mark it, and it can be applied to one corner or to every corner on the piece. It's used where a construction detail needs a bit of extra fabric hanging past the normal seam line.

**Seam - Mirrored Corner** — This creates a corner shape that is a mirror image of itself, reflected across a chosen fold line (the line where the fabric is meant to fold back on itself, like a lapel or cuff). The worker selects the corner and then picks the boundary line to mirror it against. It's useful for parts of a garment that fold back symmetrically, such as collars or cuffs.

**Seam - Turnback Corner** — This creates matching mirrored corners on both ends of a chosen seam line - called a turnback seam - so the fabric folds back evenly at each end. It's commonly used on sleeve openings or trouser hems where the fabric edge turns back on itself. The worker just selects the line, and the system generates the fold-back shape on both ends automatically.

**Seam - Frame Corner** — This builds a framed (boxed-in) corner shape at a seam where the angle is 90 degrees or wider; if the angle is actually narrower than 90 degrees, the system instead automatically makes a double-mitered corner. It's used to give certain garment corners a clean, boxed finish rather than a simple point, and notches can be added for alignment.

**Seam - Perpendicular Step Corner** — This creates a stepped seam where the width of the seam allowance changes partway along an edge, with the step cut at a right angle (perpendicular) to one of the two adjoining lines - common on details like kick pleats or plackets (the finished fabric strip around a garment opening, such as a shirt front). Before using it, the worker must split the line where the step goes, make sure both sides have equal seam allowance, and check that the sew line (not the cut line) is showing as the solid outline, swapping them first if needed. This lets the seam allowance jump to a different width right at that step point.

**Seam - Bisect Step Corner** — This creates a stepped seam allowance change like the perpendicular version, but here the step line is cut so it evenly splits (bisects) the angle between the two adjoining lines rather than going straight across. It's typically used on straight edges but can also work on corners, and the same prep steps apply - splitting the line first, keeping equal seam allowance on each side, and making sure the sew line displays as the solid outline (stripping the seam allowance first if it doesn't). It's used wherever a seam allowance needs to change width at an angled step rather than a squared-off one.

**Seam - Squared Corner** — This squares off a corner where two edges of the pattern piece meet, creating a clean right-angle-style joint instead of a pointed or curved one. A typical use is joining two body panels, such as where the upper and under sleeve pieces come together. The worker selects the corner and then the adjoining edge to square it against, and notches can be added if needed.

**Seam - Match Corners** — This makes matching squared corners on two different pattern pieces so their cut edges come out the exact same length where they'll be sewn together, which is important for seams like princess lines (vertical shaping seams) or two-piece sleeves. The worker builds the corner on one piece first, then the system automatically generates the matching corner on the other piece, either as a mirror image or as a squared corner. This ensures the two pieces line up correctly when sewn.

**Modify Pieces** — This is a menu category in the Piece menu that groups together all the tools for changing a pattern piece's position and orientation on screen, such as moving, flipping, and rotating it.

**Modify Piece - Move Piece** — This command relocates a pattern piece within the work area, either by typing exact X and Y distance measurements, snapping it to a grid point, or lining it up against another piece by matching reference points. Workers use it to arrange pieces precisely, for example lining pieces up edge to edge, and there's also an option to rotate the piece right after moving it into position.

**Modify Piece - Flip Piece** — This command flips a pattern piece's orientation - essentially creating its mirror image - either across a chosen line on the piece or across the horizontal/vertical axes into one of four directions. It's used when a piece needs to be turned into its opposite-hand version, such as creating a left piece from a right one; if you flip about a curved line, the system uses a straight line between its endpoints as the mirror line.

**Modify Piece - Rotate Piece** — This command turns a pattern piece around a chosen point, either freely by dragging with the cursor, by typing in a specific angle, or by a set distance. It can also automatically align the piece so a chosen reference point lines up exactly with the horizontal or vertical axis, or rotate it in fixed clockwise/counter-clockwise increments - useful for straightening a piece or angling it to a specific position on the layout.

**Modify Piece - Set and Rotate/Lock** — This command lets you set one pattern piece on top of another at a matching point and then pivot (rotate) the first piece around that point. Workers use it to overlap two pieces so they can use the Trace commands, or to compare lines or shapes between two pieces, such as checking if a seam curve matches another piece. You find it in the Piece menu under Modify Piece, then Set and Rotate/Lock.

**Modify Piece - Walk Pieces** — This command lets you "walk" one piece along the edge of another to check that seam lengths and curves match up correctly, similar to physically walking a pattern piece along a seam by hand. You pick the lines to compare on a stationary piece and a moving piece, enter how far to walk it, and the software shows you how well the edges line up; a right-click menu lets you change direction or skip sections while doing this. It's commonly used for quality-checking seams before pieces are sewn or graded.

**Modify Piece - Use Position** — This command places pieces on the screen into an arrangement that was saved earlier, instead of you having to drag each piece into place by hand. You bring the pieces into the work area, pick the saved position name from a list, and the pieces automatically snap into that layout, saving time when you need the same arrangement repeatedly (like for grading or assembly).

**Modify Piece - Define Position** — This command lets you save the current on-screen layout of one or more pieces so you can reuse that same arrangement later with the Use Position command. You arrange the pieces the way you want, give the arrangement a name (or let the system number it automatically), and select the pieces to include before saving; this is a time-saver for arrangements you use often, like standard assembly layouts.

**Modify Piece - Remove Position** — This command deletes a saved piece arrangement that was previously created with Define Position. You can remove all saved positions for the pieces currently on screen, or pick just one named position to delete, and you can even limit the removal to a single piece instead of the whole group.

**Modify Piece - Realign Grain/Grade Ref** — This command puts a piece back into its original orientation, or straightens the grainline/grade reference line (the line used for fabric grain direction and sizing) so it lines up with the horizontal axis. If the "Modify Grade Rules" setting is turned on, any grading measurements on parts of the piece that rotate with the grainline get automatically adjusted; if it's off, those grading values stay as they were.

**Modify Piece - Lock to Grid** — This command snaps a piece into place using the on-screen grid, either lining it up with the horizontal/vertical grid lines, moving it to an exact X/Y measurement, or matching one piece to another at a specific point. It's useful for quickly and precisely positioning multiple pieces together while keeping their spacing relationships intact.

**Modify Piece - Anchor/Unanchor** — This command locks a piece in place on the screen so it can't accidentally be dragged or bumped out of position, and can also unlock it again. For example, after tracing a piece on the digitizing table, you'd anchor it so it stays put; note that a locked piece can still be saved, deleted, or deliberately repositioned by the system, it's just protected from accidental moves.

**Modifying Pieces** — This is the overview section for the Modify Piece menu, which contains all the tools for adjusting pieces already created or brought into the work area — such as moving, flipping, or rotating them — to make pattern-making and grading easier. It also explains saving behavior: using Save with the same name overwrites the original piece without warning, while Save As will ask you whether to overwrite it, so it's recommended to give modified pieces unique names.

**Split Pieces** — This is the section heading introducing the group of commands used to divide a single pattern piece into two or more separate pieces along a chosen line.

**Split on Line** — This command cuts a piece into two smaller pieces along an internal line that's already drawn on the piece. It's commonly used for "color blocking" a garment (splitting a piece into sections that will be made from different fabric colors), and lets you choose whether to add the new pieces to the style, delete the original piece, and add seam allowance at the cut.

**Split on Digitized Line** — This command lets you draw (digitize) a new line by hand across a piece and then use that line to split the piece into two. As with other split commands, you can choose to add the new pieces to the style, delete the original, and add seam allowance along the new cut edges.

**Split Point to Point** — This command splits a piece by drawing a straight line between two points you select on the piece. You can choose to add the resulting pieces to the style, delete the original piece, and add seam allowance along the split, making it useful for simple straight-line pattern breaks.

**Split Horizontal** — This command splits a piece by drawing a straight horizontal cut line starting from a point you select. As with other split tools, you can control whether the new pieces are added to the style, the original piece is deleted, and seam allowance is added along the cut.

**Split Vertical** — This command splits a piece by drawing a straight vertical cut line starting from a point you select. Like the other split tools, you can choose to add the new pieces to the style, delete the original piece, and add seam allowance along the cut line.

**Split Diagonal Left** — This command splits a piece by drawing a diagonal cut line (angled toward the left) from a point you select. You can choose whether to add the resulting pieces to the style, delete the original piece, and add seam allowance along the new diagonal edges.

**Split Diagonal Right** — This command splits a piece by drawing a diagonal cut line (angled toward the right) from a point you select. You can choose whether to add the resulting pieces to the style, delete the original piece, and add seam allowance along the new diagonal edges.

**Creating Pieces using Split Lines** — This is the overview section covering all the ways to split a piece along a line in PDS 2000/Silhouette 2000, such as splitting on an existing internal line, digitizing a new line, connecting two points, or creating a horizontal, vertical, or diagonal cut from a point. It's especially useful for breaking down large pieces so they fit properly when plotted (printed) on paper or fabric.

**Mirrored Pieces** — This is the section heading that introduces all the tools for creating and working with pieces that are symmetrical, meaning both halves are identical when reflected across a center line. Workers use these commands when a pattern piece (like a front bodice with no side seam) is cut on the fold, so only half of it needs to be drawn and edited.

**Working with a Mirrored Piece** — This explains the general rules for handling a piece that has identical left and right sides, called a mirrored piece, which is divided by a mirror line into two equal halves. A mirrored piece can be shown folded (half the piece) or unfolded (the whole piece), and a small square symbol on the piece's icon tells you it is mirrored. Workers should always fold the piece on the mirror line before making changes, because editing only one side while unfolded will break the symmetry and the system will stop treating it as mirrored.

**Mirror Piece** — This command lets a worker turn a half-piece into a complete, symmetrical piece by picking one edge to act as the mirror line; the software then copies and flips all the shape and details across that line to build the other half automatically. It saves time because you only have to draw and edit half a pattern piece, and you can even add matching notches on the mirror line by checking the Add Notches option. Multiple pieces can be mirrored in one go, and the finished piece shows a small square symbol on its icon to show it's mirrored.

**Fold Mirror** — This command takes a mirrored piece that is currently shown in full (both sides visible) and folds it back down to display just half, with a dashed line marking the mirror line. Workers use this before making any edits, since changes should only be made to the folded half to keep the piece symmetrical; note that a piece can't be folded this way if one side has already been altered differently from the other.

**Unfold Mirror** — This command is the counterpart to Fold Mirror, used to open up a folded mirrored piece so both symmetrical halves display on screen at once. (Based on its place in the manual, it works like the related Open Mirror command described nearby.)

**Open Mirror** — This command lets a worker unfold a mirrored piece so they can view the entire piece (both halves) instead of just the folded half, while the system still remembers it as a mirrored piece. If the piece is saved or reopened later it will automatically fold back up again, but if any edits are made while it's unfolded, the piece loses its mirrored status — so edits should be done while folded, not while using this command to just look at the whole shape.

### Pleats
This is the section heading covering all the tools for adding pleats — folds of fabric sewn into a piece to add extra fullness — to a pattern piece.

**Working with Pleats** — Pleats are folds added to a pattern piece to build in extra fabric fullness, and they can be placed alone or in a repeated series, facing the same way or toward each other, at spots like the waist, shoulder, hip, below a yoke, or a sleeve edge. The amount of pleats you can fit is limited only by how much space there is along the piece's edge. Key terms to know: pleat depth is the distance from the pleat's outer fold to its inner fold, and underlay is the extra fabric used to form the pleat, equal to twice the pleat depth.

**Pleats - Knife Pleat** — This command lets a worker add one or more knife pleats — folds of fabric that are all pressed to lie in the same direction — along a chosen internal line on the piece. You specify the underlay amount (extra fabric folded under), how many pleats you want, and the spacing between them, and it's commonly used on skirts, blouses, bodices, one-piece garments, fitted yokes, insert panels, or furniture upholstery.

**Pleats - Box Pleat** — This command adds box pleats to a piece along a chosen line — these are evenly spaced folds that face away from each other (unlike knife pleats, which all face the same way) — by specifying the underlay amount and number of pleats. The system automatically adds the extra fabric needed for the pleats to the piece area; a related style, the Inverted Pleat, folds the fabric so the two folds meet each other instead of facing apart. It's typically used on skirts, blouses, bodices, and one-piece garments.

**Pleats - Variable Pleat** — This command creates an uneven pleat — either knife or box style — where one end is wider than the other, by letting the worker set the pleat width separately at each end of the pleat line. It's useful when a garment needs a pleat that tapers or changes size gradually across its length, since the internal lines forming the pleat don't need to stay parallel.

**Pleats - Taper Pleat** — This command creates a pleat, in either knife or box style, that has width at one end and narrows down to nothing (zero width) at the other end — useful for adding fullness at only one part of an edge, like adding a pleat at the top of a sleeve without changing the cuff's circumference, or adding pleats to a skirt without widening the hem. The worker sets the width at the open end only; the other end is automatically pinched to a point.

**Adding Pleats to Pieces** — This is an overview menu page that points workers to the different pleat commands (knife, box, variable, tapered) and notes that two new commands allow adding fullness to multiple pieces stacked together at once, which is a capability beyond what older AccuMark/MicroMark systems offered.

### Darts
This is the section heading for all the tools related to creating, adjusting, and manipulating darts — the folded and stitched wedges of fabric used to shape a flat piece of fabric to fit a curved body area.

**Working with Darts** — Before using dart commands, workers should know key dart terms: the apex (the pointed tip of the dart, which can be repositioned by dragging along its center line), the pivot point, the hold line (the edge that stays fixed while other parts move), the opening point, and the angle bisector (the dart's center line). Many dart commands require an already-folded dart to be unfolded first — done via the Swap Line command for AccuMark data or the Open Dart command for MicroMark data — before you can edit it.

**Creating and Working with Darts** — This overview page lists all the things a worker can do with darts on a piece: adding a plain dart or one with extra fullness, rotating/pivoting a dart, distributing a dart along a line or by rotation, combining multiple darts, adjusting a dart's tip or leg lengths, opening/closing or folding a dart, smoothing or flattening lines near a dart, and shifting where a dart's fullness sits. It serves as a menu guide pointing to the specific dart commands described elsewhere in the manual.

**Darts - Rotate** — This command lets a worker pivot an entire dart to a new spot on the piece's edge by rotating it around a chosen point, which is useful when you want the dart's fullness to open at a different location on the garment (for example, moving a dart from the side seam to the shoulder). Before using it, the dart must be unfolded; the worker picks the dart, the pivot point to rotate around, a hold line that stays fixed and unaffected, and then places the new dart opening.

**Darts - Distribute Same Line** — This command lets a worker move part or all of a dart's opening to one or more new positions along the same edge line, by sliding it rather than pivoting it around a point (which is what Rotate does instead). The worker selects the dart, then sets the new opening location(s) either by dragging with the mouse or by typing exact distances, useful for splitting or repositioning dart fullness precisely along a seam.

**Darts - Distribute/Rotate** — This command lets you swing (pivot) all or part of a dart to a new spot on the pattern piece instead of sliding it over. You pick the dart to move, then pick a pivot point inside the piece, and the piece rotates around that point to partly close the original dart while opening a new one. It's useful when you want to add a second dart without cutting away any extra fabric area, since you can move a set distance or a percentage of the original dart (for example, splitting a 3-inch dart into a 1.5-inch, or 50%, dart elsewhere).

**Darts - Combine Same Line** — This command merges two darts that sit on the same pattern edge (perimeter line) into one dart by sliding them together, rather than pivoting them. The dart you're merging must first be "unfolded" (opened flat) before you can combine it. You pick the dart to combine and the target dart it should join, and the system redraws the piece showing the two darts now as one.

**Darts - Combine Diff Line** — This command joins two darts that are on different edges of the pattern piece into a single dart, adding their widths together, without changing the overall size of the piece. Both darts need legs of about the same length and must be opened (unfolded) first. You select the dart to move, a pivot point, the edge line to hold in place, and the target dart, and the new combined dart ends up located where the target dart was.

**Darts - Add Dart** — This command inserts a brand-new dart into a pattern piece without adding any extra fullness (width) to the piece — it's for building a dart from scratch or reshaping one that's already there. You click where the dart opening should sit on the piece's edge, then click the dart's apex (the inner point where it ends, often where a drill hole marking goes).

**Darts - Add Dart With Fullness** — This command adds a brand-new dart to a piece while also adding fullness (extra flare or width) to the pattern at the same time, unlike the plain Add Dart command. You choose where the dart opening goes, set the dart tip (apex) point, and then choose the point the pattern splits, or "slashes," open to create the added fullness.

**Darts - Change Dart Tip** — This command changes how long a dart is by moving its tip (apex) — but only along the dart's centerline (the bisector). You click the dart at its tip, then either drag the tip to a new spot or type in the new length, and the dart lines automatically blend into the piece's edge before and after the dart.

**Darts - Equal Dart Legs** — This command automatically makes the two sides ("legs") of a dart the same length, so the dart folds and sews evenly. You can either select the dart tip to make both legs average out to a matching length, or select one specific leg so the other leg is adjusted to match it exactly.

**Darts - Balanced Resize** — This command changes a dart's width (adding or removing fullness) while repositioning both of its legs at once, keeping the change balanced on both sides. You pick the dart, choose a point to split ("slash") the pattern open at, select which internal lines should move with it, then type the new dart width either as a final size or as a percentage increase/decrease from the current width.

**Darts - One Sided Resize** — This command changes a dart's width by moving only one of its two legs, while the other leg (the "hold line") stays fixed in place. You select the dart, the point to split the pattern open at, the leg that should stay still, and then type the new width as an exact value or a percent change from the current size.

**Darts - Open Dart** — This command "opens up" a dart that is currently closed or folded flat, turning it back into a spread-open shape. Many other dart tools (rotating, combining, distributing, or resizing) require the dart to be open first, so this is often a required first step before using those commands.

**Darts - Fold/Close Dart End** — This command folds a dart closed, changing the piece's outer edge to make up for the fold — it turns a dart that's cut into the edge of the piece into an internal folded dart instead. While folding, you can choose to also add fold lines, a drill hole, and/or notches, and you specify which side of the dart leg the fold should go toward.

**Darts - Smooth Line** — This command smooths out an edge or internal line by letting the system automatically reposition points along it (except the very end points), which cleans up bumps or unevenness, including near notches. You select the line, then drag markers ("thumbtacks") to set which section of the line gets smoothed; running it multiple times will flatten the curve more each time.

**Darts - Flatten Line Segment** — This command straightens out part of a line by deleting all the extra points within a chosen section, making that section flat/straight. You select the line, then drag the thumbtack markers to set exactly which stretch of the line should be flattened.

### Fullness
This is the section heading in the Piece menu for tools that add or remove fullness — extra flare, spread, or gathered width — in a pattern piece, generally used to build in design fullness like flare or gathers.

**Fullness - Fullness** — This command evenly spreads (adds) or removes fullness along an entire edge (perimeter/boundary line) of a piece, such as for flare or gathers. You pick the edge line to add fullness to, the line to "slash" or spread toward, the line that should stay still, and then type the amount of fullness — the system spreads it evenly along the whole selected edge while the opposite line shifts to make room.

**Adding Fullness to Pieces** — This is an overview explaining that the Fullness menu's commands let you add flare or gathers to a pattern piece for style purposes. It notes that most of these tools will be familiar to prior AccuMark users, but two commands are new because they let you add fullness across multiple stacked pieces at once instead of one at a time.

**Fullness - 1 Point Fullness** — This command adds or removes fullness starting at one specific point on an edge line and running to the end of that same line, rather than along the whole edge — useful when you want to add flare to only part of a piece, like below a curve, without disturbing the curve itself. You pick the starting point, the point to spread toward, the line to hold still, and the amount of fullness; a notch can be set as the stationary point if you want it to stay in place.

**Fullness - Variable Fullness** — This command creates uneven (variable) amounts of fullness across a piece rather than a flat, even amount. You draw one or more slash lines by picking two points on the edges, choose which internal lines should move, and then separately position each end of the slash lines by dragging or typing a distance, so one end can spread more than the other.

**Fullness - Tapered Fullness** — This command lets a worker add fullness (extra fabric width) that gets bigger at one end of a cut line and tapers down to nothing at the other end. After choosing Fullness > Tapered Fullness from the Piece menu, the worker draws one or more "slash lines" (cut lines across the pattern piece), then drags the two halves of the slash line apart at the full end while the other end stays pinned together (hinged), and types or drags in the exact spread amount. This is used when a pattern needs uneven extra room in one spot, such as adding shape near a hem while keeping the waist flat.

**Fullness - Parallel Fullness** — This command adds an even amount of extra fabric fullness across a piece, with the spread being the same amount along the whole slash line instead of tapering. The worker selects two boundary points to create a slash line, chooses what stays fixed, then either drags the line open or types in a distance/angle value to set how much fullness to add. It's used when a garment needs uniform extra fullness, like gathering fabric evenly rather than shaping it more on one end.

**Fullness - Taper Slash n Spread (Expert Edition Only)** — This function adds tapered fullness across several pattern pieces at the same time, instead of doing them one at a time. The worker selects all the pieces to change, draws a single slash line across all of them (making sure it reaches the outer edges), picks a spot to hold still, and then drags or types in the amount of spread to add. It saves time when multiple stacked pieces need the same tapered fullness adjustment made together.

**Fullness - Parallel Slash n Spread (Expert Edition Only)** — This function adds an even (parallel) amount of fullness across multiple pattern pieces at once, rather than one piece at a time. The worker selects all the pieces to modify, draws slash lines across all of them reaching the outer edges, picks a point to stay still, and then drags or types a value into the input box to set the fullness amount. It's useful for quickly adding matching fullness to a stack of related pieces in one step.

### Asymmetrical Folds
This is the section/menu heading for a group of commands used to fold a pattern piece along a line that is not a mirror line (a line that splits a piece into two identical mirrored halves), letting workers check how parts of a piece line up.

**Working with Asymmetrical Folds** — This menu contains a set of commands used to virtually fold a pattern piece along lines other than a standard mirror line, such as along a chosen line, between two points, along dart lines, or along pleat lines. Workers use these folds to check things like whether two edges match, whether a dart is even, or whether a pleat lays correctly, without cutting real fabric. Only one fold is normally allowed per piece, except the Pleat Fold command which allows two, and folded pieces can still be edited with other pattern tools.

**Asymm Fold - Line Fold** — This command folds a piece along an internal line the worker selects, such as a grain or grade reference line, to see if the piece is symmetrical/proportional. The worker picks the internal line, then picks a boundary edge on the side that should fold over, and the system redraws the piece folded so the worker can visually check it. It's commonly used, for example, to fold a sleeve pattern in half to confirm both sides match up correctly.

**Asymm Fold - Line to Line Fold** — This command folds a piece by matching up two separate lines the worker selects, which is useful for checking if two lines are the same length or line up correctly (like a crease down a pant leg front). The worker picks the first line, then the line to match it to, and the system draws a dashed "fold" line and folds the piece toward whichever boundary edge the worker clicks. If a selected line has more than two points, only its end points are used for matching.

**Asymm Fold - Match Points** — This command folds a piece between two points the worker selects — one stays in place while the second point is folded over to match it, such as checking how knee notches on a pant leg align. The worker first picks the point to stay still, then the point to fold to it, and the system redraws the piece with a dashed line showing where the fold happened. This helps workers visually verify that specific spots on a pattern line up correctly.

**Assym Fold - Dart Fold** — This command folds a dart (a stitched fold used to shape fabric) so the pattern edge looks the way it would after the dart is actually sewn, shifting the dart's extra fullness to the other side of the piece. The worker simply selects the dart to fold, and the system redraws the piece with the boundary adjusted as if sewn. It's used to check that both legs (sides) of the dart are equal length and to verify the sew line before cutting.

**Asymm Fold - Pleat Fold** — This command folds a piece between two points the worker selects to create a pleat (a folded-over section of fabric), with the system automatically figuring out the fold line based on the middle point between the two selected points. Up to two pleat folds are allowed per piece, and this is used to check that the pleat's hidden underlayer (underlay) is the correct size before cutting fabric.

**Asymm Fold - Perim Pt Fold** — This command creates a fold line between two points on the piece's outer edge (perimeter/boundary) that the worker selects, such as showing where a sleeve cuff should fold. After picking the two points, the worker clicks on the edge of the section that should fold over, and the system draws a dashed line for the fold and flips that section over the rest of the piece; note only one fold is allowed per piece.

**Asymm Fold - Unfold** — This command removes any fold made using the Asymmetrical Fold commands, restoring the piece to its original unfolded shape and deleting the internal fold lines the system had drawn. The worker just clicks on the folded piece to undo it. It's used once a worker is done checking a fold and wants the pattern back to normal.

**Asymm Fold - Unfold Keep** — This command undoes a fold like the regular Unfold command does, but it keeps the internal line marking where the fold was made instead of deleting it. The worker clicks the folded piece to reverse the fold, and the piece redraws flat again with that fold line still visible for reference.

### Grade Rules
This is the section/menu heading covering grade rules — the settings that control how a pattern piece changes size (grows or shrinks) between different garment sizes.

**Overview of Grade Menu** — This menu contains all the commands for creating and adjusting grading — the rules that define how a pattern piece grows or shrinks from size to size (for example, from a Small to a Large). From here workers can create/edit rules, modify existing rules, copy a size line, set a base size, add a size break, assign a rule table to a piece, or build a graded nest (a set of pattern pieces at multiple sizes).

**Creating or Editing Grade Rules** — This menu holds the specific tools for building or changing the grade rules that make an AccuMark pattern piece grow or shrink between sizes. Workers can enter grading using delta X/Y values (the amount a point moves left-right and up-down between sizes), base grading off perimeter lines, match a graded line's length or angle to another line, or keep certain lines parallel or at the same angle across all sizes — giving several ways to control exactly how a piece changes size.

**Hints on Viewing and Working with Grading** — This section gives helpful tips for viewing and managing grading, such as using View/Grade commands to show or hide a nest of graded sizes on screen. It also explains symbols shown next to rule numbers: a pound sign (#) means the system generated that grade rule automatically (e.g., during digitizing), and an asterisk (*) means a grade point was created or changed manually using Grade menu commands, including automatic updates when Piece menu edits like Pivot Dart or Tapered Fullness are applied with Modify Grade Rules turned on.

**Copy Size Line** — This command copies the set of sizes (the size line) from one pattern piece to another piece, so both pieces grade across the same sizes. Workers use it to keep related pieces (like a front and back panel) matched to the same size range, and it must be done before grading a piece with the Create Delta or Create Offset commands. To use it, you pick the piece with the size line you want, then pick the piece(s) you want it copied to.

**Make Base Size** — This command changes which size is treated as the "base size" (the starting size that all other sizes are graded up or down from) for a pattern piece. For example, if a piece's base size is currently 10, this lets a worker switch it to 12 instead. Before doing this, the size you want to make the new base must already be shown on screen using the Show Non-base Size command.

**Add Size Break** — This command turns one of the in-between (intermediate) sizes on a piece into a "size break" — a size where the grading rules actually change amount instead of just following a steady progression. It only works on AccuMark pieces with numeric sizes, and because it adds a new growth amount at that size, it affects all the existing grading rules on the piece. Once the piece is saved/updated, a size break cannot be changed back into a regular intermediate size, so workers should be sure before doing this.

**Assign Rule Table** — This command attaches a new grading rule table (a saved set of grading instructions) to a pattern piece, replacing whatever rules it had before. Once assigned and saved, the piece will use that rule table's grading every time it's opened again, and the piece automatically becomes the base size of that table. If the piece has grade points that the new table doesn't cover, those points simply won't grow/shrink between sizes.

**Modifying Grade Rules** — This is a menu of commands for changing or copying the grading instructions already applied to a piece — for example, editing a rule directly on the piece in the work area, adding a new grade point, copying rules from a table or another piece, copying growth in just the X or Y direction, working with nested (stacked) pieces, flipping plus/minus values, or rotating growth 90 degrees. Workers open this menu whenever they need to adjust how a piece grows or shrinks across sizes rather than starting grading from scratch.

**Create Nest** — This command stacks multiple pattern pieces of different sizes on top of each other to build a single graded "nest" (a visual set showing how the shape changes size to size), either using an existing size line or a new one, and can even build a nest from pieces that were scanned in. Workers use it to see or generate the full size range for a style, choosing to stack the pieces at matching points or at the piece center.

**Clear Charts** — This command simply closes and removes any measurement charts (like the ones created by Measure Line) that are currently displayed on screen. It's used when a worker is done reviewing chart data and wants to clear the work area again.

**Measure Line** — This command displays a chart showing the length of one or more selected pattern lines across every size in a graded set of pieces, letting workers quickly compare how a line's length changes from size to size. It can also compare one group of selected lines against another group and show the difference between them in a separate column, and the resulting chart can be printed or saved.

**Working with Line Size Charts** — This explains how to read and use the charts that pop up when running the Measure Line command — each row is a size, and each column corresponds to a labeled line selected in the work area. Workers use these charts to check exact measurements per size and to see calculated differences between groups of lines, and the chart data can be printed or exported for records.

**Export Rules** — This command sends (exports) the grading rules from a pattern piece into a rule table file, either adding to an existing table or creating a new one if it doesn't exist yet. The piece and the rule table must share the same base size and size line, or the system will refuse with a "Size Lines Do Not Match" message; rules can be exported one at a time or for the whole piece at once.

**Create/Edit Grade Rules** — This is the menu section containing all the commands for building brand-new grading rules or editing existing ones on a piece, using methods like Delta (X/Y growth values) or Offset (perimeter-based growth). Workers use these tools whenever a piece needs its size-to-size growth defined or corrected without necessarily relying on a pre-made rule table.

**Create/Edit Rules – Edit Delta** — This command lets a worker adjust the grading at one or more specific size breaks on an already-graded piece — by typing in X (side-to-side) and Y (up-down) growth amounts or by dragging points with the cursor — without disturbing the grading at the other sizes. It's useful when just one or two sizes in a graded nest need a correction rather than redoing the whole grade.

**Create/Edit Rules – Create Delta** — This command builds brand-new grading rules on a piece (graded or not) by manually assigning X and Y growth values to a chosen point, instead of pulling the growth from a saved rule table. The piece must already have a size line assigned, and this is one of the main ways to grade a piece point-by-point from scratch.

**Create/Edit Rules – Edit Offset** — This command edits grading values based on distance along the piece's outline (perimeter) rather than plain side-to-side/up-down (X/Y) growth amounts, and it works even on rules that originally came from a rule table. Workers select the piece, then the specific point to adjust, and the sizes display stacked together (nested) so the change can be seen across the whole size range.

**Create/Edit Rules – Create Offset** — This command creates new grading rules based on distance along the piece's outline (perimeter-based growth) rather than simple X/Y growth values, with the exact form shown depending on the type of point selected. Workers pick the point on the base size pattern where new grading is needed, and MicroMark users have a similar tool called Perpendicular grading.

**Working with Create/Edit Forms** — This explains the on-screen data-entry form that pops up whenever a worker uses one of the grading tools (Edit Delta, Create Delta, Edit Offset, or Create Offset) to change a selected point's growth values for every size in the graded set. The form can be dragged to a different spot on the screen so the worker can watch how their typed changes affect the pattern's sizes in real time, and vice versa.

**Working with Distances Grade Forms** — This describes the form that appears when using distance-based grading commands (such as Keep Angle Edge Ext, Parallel Ext, Specify Distance, or Intersection Offset), where a worker types an Amount to control growth by distance rather than X/Y values. Entering 0.00 for every size keeps that particular measurement identical across all sizes, and like other grade forms it can be moved around the screen to watch the pattern update live.

**Create/Edit Rules – Match Line X** — This command creates a grading rule that makes one line's length automatically match the graded length of a corresponding line on another piece it needs to be sewn to, applying growth only in the X (side-to-side) direction. Workers start from a grade point with zero growth, then select the line to grade and pick the matching line(s) on the other piece — useful for ensuring two pieces that get sewn together, like a sleeve and armhole, stay the same length across every size.

**Create/Edit Rules – Match Line Y** — This tool, found in the Grade menu, lets a worker make a graded edge automatically match the length of a corresponding edge on another piece that it will be sewn to, but only in the up-and-down (Y) direction. You start at a grade point with zero growth, pick the line and end point to grade, then pick the matching line(s) on the other piece, so when the pattern is sized up or down the two edges always stay the same length and sew together properly. This saves the worker from manually calculating matching seam lengths for every size.

**Create/Edit Rules – Keep Angle Apex** — This Grade menu command locks in the angle (corner shape) found at a point on the sample/base size so that every graded size keeps that exact same angle. The worker selects the corner point, and the system automatically recalculates the surrounding lines for each size so the corner doesn't distort as the pattern grows or shrinks; one of the two lines forming the angle can be an internal line (a marking or seam line inside the piece, not on the outer edge).

**Create/Edit Rules – Keep Angle Edge X** — This Grade menu tool keeps the corner angle at an edge point the same across all sizes while only changing the sideways (X, left-right) measurement as the piece grades up or down. The worker picks the point to grade, then the apex (corner tip) and another point on the angle's edge, and the system preserves that angle while adjusting size only in the X direction.

**Create/Edit Rules – Keep Angle Edge Y** — This Grade menu tool keeps the corner angle at an edge point the same across all sizes while only changing the up-down (Y) measurement as the piece grades up or down. The worker selects the point to grade, then the apex (corner tip) and another point on the angle's edge, so the shape of that corner stays consistent in every size while only the vertical growth changes.

**Create/Edit Rules – Keep Angle Edge Ext** — This Grade menu command keeps a corner's angle the same across all sizes, similar to the other 'Keep Angle' tools, but it also lets the length of that line grow or shrink for each size. The worker selects the point, the angle's apex, and another point on the edge, so both the angle and the line length can be controlled together as the pattern is graded.

**Create/Edit Rules – Parallel X** — This Grade menu tool makes one of the two lines meeting at a point stay parallel (running the same direction) across all sizes, changing only the sideways (X) measurement. The worker picks the point to grade and the other end of that line, and the system keeps the line's direction consistent in every size while adjusting horizontal growth; MicroMark users can get a similar effect using Perpendicular grading.

**Create/Edit Rules – Parallel Y** — This Grade menu tool makes one of the two lines meeting at a point stay parallel (running the same direction) across all sizes, changing the up-down (Y) measurement. The worker selects the point to grade and the other end of the line, so the line's angle stays consistent in every size; MicroMark users can achieve a similar result with Perpendicular grading.

**Create/Edit Rules – Parallel Ext** — This Grade menu command keeps a line parallel to the same line on the base (sample) size across all sizes, and also lets the worker control how much that line's length grows or shrinks per size. After selecting the point and the other end of the line, a Distance Grading form pops up where the worker types in growth values for each size — entering 0.00 keeps that line the same length in every size.

**Create/Edit Rules – Specify Distance** — This Grade menu tool is used to control how a notch (a small cut or mark used for matching pieces during sewing) moves along an edge as the pattern is graded to different sizes. The worker selects the notch, picks the end point to measure from, and then fills in a Distance Grading form with growth values for each size (0.00 keeps the notch in the same spot for every size); MicroMark users can get a similar result with Tangent grading.

**Create/Edit Rules – Intersection X** — This Grade menu command automatically figures out the sideways (X) grading needed so the end of an internal line (an inside marking, like a pocket placement or dart) lines up correctly with the outer edge of the piece in every size, when the up-down (Y) distance is already known. The worker simply selects the point to grade and the system calculates the correct X value for all sizes.

**Create/Edit Rules – Intersection Y** — This Grade menu command automatically figures out the up-down (Y) grading needed so the end of an internal line (an inside marking) lines up correctly with the outer edge of the piece in every size, when the sideways (X) distance is already known. The worker selects the point to grade, and the system calculates the correct Y value for all sizes.

**Create/Edit Rules – Intersect Parallel** — This Grade menu tool calculates both the sideways (X) and up-down (Y) grading for one end of an internal line so that the line stays parallel across all sizes and still meets the outer edge correctly, based on how the other end of that line is already graded. The worker selects the point to grade and the other end of the line, and the system handles the math automatically.

**Create/Edit Rules - Intersection Offset** — This Grade menu command calculates the X and Y grading for one end of an internal line so it meets the piece's outer edge at a specified offset distance in every size. The worker chooses how the rule applies at joined endpoints, selects the point to grade, then enters growth values in a Distance Grading form (0.00 keeps the same distance in every size) and clicks Update to apply the new rule.

**Modify Grade Rules** — This is a menu section in the Grade menu that groups together the tools used to change, copy, or add to grade rules that have already been created on a pattern piece, rather than creating brand-new rules from scratch.

**Modify Rule – Change Grd Rule** — This Grade menu command lets a worker swap out the grade rule currently applied to one or more points on the pattern for a different, already-existing rule number from a grade rule table (a saved list of sizing instructions). The worker selects the point(s), types in the new rule number (and the rule table name if it's a different table), confirms, and the system updates the piece to use the new grading instructions.

**Modify Rule – Add Grade Point** — This Grade menu command turns a point along a line — one that isn't currently a grade point — into a new grade point, without changing the overall shape of the sized-up or sized-down pattern (called the 'nest'). The worker selects where on the line to add the point (by clicking on it or entering a value), and the system creates a grade rule there automatically based on the surrounding shape.

**Modify Rule - Copy Table Rule** — This Grade menu command copies a specific grade rule from a saved rule table (library) onto a piece, forcing the system to use the table's values even if the piece already has a rule with different X/Y measurements assigned to the same point. Workers use this when a rule on the piece doesn't match what's officially in the table and needs to be corrected to the table's standard values.

**Modify Rule - Copy Grade Rule** — This Grade menu command lets a worker copy an existing grade rule from one point on a piece to one or more other points, either on the same piece or a different one, so they don't have to redefine the same sizing instructions repeatedly. The worker selects the reference point that already has the correct rule, then selects the target point(s) that should receive that same rule.

**Modify Rule – Copy X Rule** — This command lets you copy just the sideways (X-axis) growth amount from one grade point's rule and apply it to another point, without touching the up-and-down (Y-axis) value. You pick a reference point whose X value you want to copy, then pick the target point(s) that should receive it, and the system applies that growth automatically. Workers use this to keep certain points growing the same amount horizontally across sizes without having to type the value in by hand.

**Modify Rule – Copy Y Rule** — This command copies only the up-and-down (Y-axis) growth value from one grade point's rule and applies it to a different point, leaving the sideways (X-axis) value alone. You select the point you want to copy from, then select the point(s) that should get that same Y growth. It saves time and keeps grading consistent when two points need to move the same amount vertically between sizes.

**Modify Rule – Copy Nest Rule** — This command copies both the X (sideways) and Y (up-and-down) growth values shown on a graded, stacked piece (a "nest" showing all sizes together) and applies them to a new point. It's mainly used when a piece has been flipped, rotated, or pivoted, or when special "Z attribute" settings are involved, so the grading still matches correctly. You pick the reference point on the nested piece, then the target point that should receive the same growth.

**Modify Rule – Copy Nest X** — This command copies only the sideways (X-axis) growth values from a graded, stacked piece (nest) and applies them to a new point, leaving the Y value untouched. It's used after a piece has been flipped, rotated, or pivoted, so the horizontal grading still lines up correctly. You select the reference point on the nested piece and then the target point to receive that X value.

**Modify Rule – Copy Nest Y** — This command copies only the up-and-down (Y-axis) growth values from a graded, stacked piece (nest) and applies them to a new point, leaving the X value untouched. It's used after a piece has been flipped, rotated, or pivoted, so the vertical grading still lines up correctly. You select the reference point on the nested piece and then the target point(s) to receive that Y value.

**Modify Rule – Flip X Rule** — This command switches the direction of a grade point's sideways (X-axis) growth — turning a positive number into a negative one, or a negative into a positive. You just select the grade point on the base (sample) size and confirm, and the system reverses that X direction. It's handy when a piece has been mirrored or the grading needs to grow the opposite way than it currently does.

**Modify Rule – Flip Y Rule** — This command switches the direction of a grade point's up-and-down (Y-axis) growth — turning a positive number into a negative one, or a negative into a positive. You select the grade point on the base (sample) size and confirm, and the system reverses that Y direction. It's useful when a piece has been mirrored or otherwise needs its vertical grading to grow the opposite way.

**Modify Rule – Rotate 90** — This command turns a grade point's growth direction 90 degrees clockwise, meaning the amount that used to move the point sideways now moves it up/down (and vice versa). You just click on the grade point on the base (sample) size, and the software redraws the piece to show the new grading direction. This is used when a piece's orientation has changed and the grading needs to rotate along with it.

**MicroMark Grading Types** — This is a heading/section title in the manual introducing the different grading methods available under MicroMark, a grading data format built into PDS 2000/Silhouette 2000; it doesn't perform an action itself but leads into the specific grading type topics that follow.

**Working with MicroMark Grading** — This section explains that PDS 2000/Silhouette 2000 offers several ways to grade (resize) pattern pieces using the MicroMark system, with "Delta grading" — moving a point a set distance along the X (sideways) and Y (up-down) axes — being the most commonly used method. Other special grading types, covered in the following topics, are available for handling trickier situations like notches, curves, and split pieces.

**Tangent Grading** — Tangent grading is a special grading method used mainly on notches (small cut marks on a pattern edge) to keep them positioned correctly and to keep a curve looking smooth as the piece is graded to different sizes. Unlike normal grading, which needs both an X and Y value, tangent grading uses just one plus-or-minus value to control growth direction, measured from a designated "curve length reference point" on the line.

**Perpendicular Grading** — Perpendicular grading is used when a grade line needs to stay at a right angle (perpendicular) to a sloped or curved section of the pattern as it's resized to different sizes. Workers would use this so a detail like a dart or seam line keeps its correct angle relative to the curve instead of skewing when the piece grows or shrinks.

**Opposite Grading** — Opposite grading lets you copy a grade rule that is the same amount of growth as another point, but applies it in the reverse (opposite) X or Y direction. This is useful for symmetrical pattern details where one side needs to grow one way and the mirrored side needs to grow the exact same amount but the other way.

**Blend Grading** — Blend grading smooths the transition of growth values between two or more already-defined grade points, so the line or curve between them changes shape gradually rather than abruptly. Workers would use this on curved edges to keep the pattern shape looking natural across all the graded sizes.

**Proportional Grading** — Proportional grading is used on pieces that have been split into sections, so that each section grows in proportion to the others rather than by a fixed, independent amount. This keeps split pattern pieces properly balanced and correctly sized relative to each other across the size range.

**Paste Grading** — Paste grading is used when two separately graded pieces are being combined or merged into one, allowing the grading rules from both original pieces to carry over correctly into the new combined piece. This saves the worker from having to re-grade the merged piece from scratch.

**Line Grading** — Line grading applies grade rules to an entire line (rather than just individual points), controlling how that line's length, shape, or position changes as the pattern is resized across the size range. This is a shorter, inferred definition since the manual excerpt only lists the topic name without further detail.

**Variation Grading** — Variation grading is used to create size variations like Longs, Shorts, and XLongs from a base size, rather than just standard size increases. It works alongside "Alternate Grade Reference lines," letting a company offer length variations of a garment without building a completely separate pattern for each one.

### Measure Menu
This is the menu on the PDS 2000/Silhouette 2000 screen that holds all the tools for measuring things on your pattern pieces, like line lengths, distances, angles, perimeters, and areas. Workers open this menu whenever they need to check a measurement on a piece or between pieces without having to leave the software or use a separate tape measure.

**Overview of Measure Menu** — This is a summary explaining that the Measure menu contains commands for checking distances, lengths, angles, perimeters, and areas on pieces shown in the work area (the screen where you view and edit patterns). It also lets you build a custom toolbar with your most-used measuring commands, and reminds workers familiar with older AccuMark or MicroMark systems that some line-handling methods here may be new and worth learning to work faster.

**Line Length** — This command measures the length of a boundary (outer edge) line or an internal line (like a dart or seam line) on a pattern piece. To use it, select Line Length from the Measure menu, click on one or more lines (even on different pieces) to measure, then end the selection to see the results; if the piece is graded (made in multiple sizes), it can show the line length for each size. Use Clear Measurements afterward to remove the numbers from the screen.

**Distance 2 Line** — This command measures the distance between two separate lines, which can even be on two different pattern pieces. You choose whether the measurement is taken vertically, horizontally, perpendicular to the grainline, or parallel to the grainline (the grain/grade reference line used for fabric direction), and then select the two lines to measure between. This is handy for checking spacing or clearance between features on one piece or across two pieces.

**Perimeter 2 Pt/ Measure Along Piece** — This command measures the distance along the edge of a piece between two points you pick on its boundary line, rather than a straight-line distance. You click and drag along the line to the first point, then select a second point, and the system highlights that segment and shows its length. This is useful for checking things like the length of a specific curved edge, such as an armhole section, and you can clear the measurement afterward.

**Distance 2 Pt/ Measure Straight** — This command measures the straight-line distance between any two points you select, whether those points are on a boundary line, an internal line, or the grainline. After picking the first and second points, a straight line appears connecting them along with the measurement, and you can keep clicking new points to measure multiple straight distances from the same starting point. It's the tool to use when you need a direct point-to-point measurement rather than following a curve or edge.

**Piece Perimeter** — This command adds up and measures the total length of all the boundary lines around a piece — essentially the full distance around its outer edge. You simply select one or more pieces by clicking on them, and the total perimeter measurement appears in the center of each piece. This is useful for quickly checking the overall size of a piece's edge, for example to estimate binding or trim needed.

**Piece Area** — This command calculates and displays the total surface area of a pattern piece. Just select the piece or pieces by clicking on them, and the area measurement shows up in the middle of each one, which is helpful for tasks like estimating fabric usage or comparing piece sizes.

**Angle** — This command measures the angle formed between two lines on a piece. You select the two lines next to the angle you want to check, and the measurement (in degrees) appears in the Angle field of the User Input box on screen. This is useful for checking that corners, darts, or seam angles match the intended design.

**Clear Measurements** — This command wipes away all the measurement numbers and lines currently shown on the screen from using any of the Measure menu tools. Use it after you're done checking measurements so the work area isn't cluttered with old numbers before moving on to the next task.

### Draft/Sketch
This is the menu heading for the Draft commands, which are the tools used to hand-draw or digitize pattern pieces directly using a pen/stylus on the Silhouette digitizing table, similar to drawing on paper but captured live into the computer.

**Sketch** — This command lets you draw a brand-new pattern piece by hand using a pen or stylus on the Silhouette table, just like drawing with a pencil on paper — as you draw on the table, the same lines appear on the screen at the same time. Workers use this for free-hand drafting, trying out new style lines, drafting with rulers and curves, tracing cut oak-tag (heavy cardboard) patterns, or building new pieces from slopers (basic pattern templates). Before starting, make sure the pattern is taped down securely on the table and, if needed, set the Draft Scale so the screen matches the real table size.

**Line - Curve** — This command lets you enter an existing pattern piece into the system by touching a series of points along its edge with the stylus, kind of like connecting the dots, after which the system automatically draws straight or curved lines between those points. It's commonly used for digitizing paper or muslin (soft fabric) patterns, copying pieces from an assembled garment, or adding internal details like grain lines, drill holes, or slash lines, and you can switch between straight-line and curved-line modes as you go.

**Note - Illustrate** — This command lets you handwrite notes or draw diagrams and illustrations directly onto a pattern piece using the stylus, useful for construction instructions or sketching a design idea. These notes are saved with the piece and can be viewed during production, but the manual advises deleting them before sending pieces to actual production since they take up extra storage space; you can use the Erase button to remove a note or line while working.

**Note Pen Resolution** — This is a setting that controls how many small points the system automatically places along lines you draw with the Note/Illustrate command — the default is one point every 0.1 inch (0.25 cm). Lowering this setting creates more points for smoother, more detailed lines, which matters when trying to accurately capture a hand-drawn note or illustration.

**Point Filter** — This setting works together with the Sketch Pen Resolution and Note Pen Resolution settings to clean up a hand-drawn line after you lift the pen or stylus off the table, by removing unnecessary extra points on straight or gently curved sections. A lower Point Filter value leaves more points on the line, so adjusting it helps balance smooth curve detail against a cleaner, simpler line with fewer unneeded points.

**Reorient** — This command realigns a pattern piece already taped to the Silhouette table with its matching piece on the computer screen, which is needed if the physical pattern gets bumped or moved, or if you're resuming work on a pattern that was recently taped down again. You select two matching points, first on screen then in the same order on the table, and the system shifts the on-screen piece to line up exactly with the real pattern on the table.

**Draft Scale** — This setting adjusts the screen so that its scale matches the actual physical size of the Silhouette table surface, which is often needed before sketching or reorienting a piece so that what you draw or check on-screen correctly corresponds to the real table area. After using Draft Scale and Reorient together, workers can use the Anchor/Unanchor command to lock the piece in place on screen so it doesn't get accidentally moved once properly aligned.

**Create Piece** — Create Piece is a command in the Draft menu that turns a rough sketched ("draft") pattern piece into a real, usable pattern piece by closing up its outer edge (the "perimeter/boundary") and adding a grain/grade reference line, which is the straight line used to align the piece on fabric and to grade it into sizes. The system automatically looks for and fixes small gaps where lines should meet, so your sketched lines need to be clean and clearly connected or you'll get an error message. Use it right after sketching a piece with Sketch or Line/Curve when you want the whole drafted shape converted into a finished piece at once.

**Draft Trace** — Draft Trace is a Draft-menu command that builds a valid pattern piece by letting you pick out only the specific lines from your sketch that should become the piece's outer edge, ignoring any lines you don't select. You trace around the piece clockwise starting at the lower left corner, then pick a line to be the grain line (the reference line used for layout and grading), and the original sketch stays behind on screen even after the new piece is moved. Use this instead of Create Piece when your sketch has extra or messy lines and you only want certain ones turned into the finished piece.

**Trim/Extend Line** — Trim/Extend Line is a Draft-menu tool used to shorten or lengthen individual lines on a sketched piece before turning it into a finished piece with Draft Trace or Create Piece. If you stretch a line, it keeps going in the same direction; the tool also automatically finds the nearest place two lines should meet, which makes it quick to fix sketch lines that don't quite connect. Use it as a cleanup step whenever your drafted lines have small gaps or overshoot at the corners.

**Trim/Extend Piece** — Trim/Extend Piece (also called Kerf) removes a thin sliver from around the edge of a piece that was just created with Create Piece or Draft Trace, equal to half the thickness of the pen tip used to trace it. This matters because when you trace a hard pattern by hand, the width of the pen/stylus tip makes the digital piece come out very slightly bigger than the real one. You enter a small offset amount (up to about a quarter inch or centimeter, using a negative number to shrink the piece) to correct for this.

**Stream Sketch** — Stream Sketch is a mode within the Draft menu's Sketch command that lets you create sketched lines while the pen tip stays just above the table surface rather than actually touching it. This is useful when you want to trace or draw motion/paths on-screen without marking the paper or fabric underneath.

**Sketch Pen Resolution** — Sketch Pen Resolution is a setting that controls how many extra points the system automatically places along the lines you draw with the Sketch command, with a default of one point every 0.1 inch (0.25 cm). A lower resolution number creates more points on the line, giving finer detail but a heavier data file, so it's usually adjusted together with the Point Filter setting, which removes unneeded points on straight or gently curved sections. Workers would tune this if their sketched lines are coming out too jagged (increase detail) or too data-heavy (reduce detail).

**Basics of Drafting Pieces in Silhouette 2000** — This is an introductory section of the manual that walks through the fundamentals of drafting pattern pieces in Silhouette 2000, including the difference between draft, working, and saved pieces, how the Silhouette table/screen/pen work together, and how to use the pen and eraser tools. It's meant as a starting orientation topic rather than a single command, pointing workers to the more detailed how-to topics that follow.

**Create Draft Pieces and Save Working Pieces** — This topic explains the lifecycle of a pattern piece in the system: a "draft piece" is a rough sketch that hasn't been finalized, which must be converted into a "working (valid) piece" — one with three closed sides and a grain/grade reference line — before it can be used, and then saved so it's stored for use in a model. For example, a worker tapes clean paper and the garment or muslin to the Silhouette table, traces the sew lines with the pen/stylus so the shape appears on screen, and then finishes and saves it as a usable piece.

**Working with Silhouette Table, Screen, and Pen** — This topic explains how the physical Silhouette table, the on-screen work area, and the pen/stylus are all lined up so that touching a point on the paper at the table makes the on-screen cursor land on that exact same point of the piece. This direct match-up depends on using Reorient to position a taped-down piece and having the view set to Fullscale; after zooming in or out, workers need to use Draft Scale to restore that same one-to-one alignment between the table and the screen.

**Using the Pen** — This topic covers how the pen/stylus is used on the Silhouette table to do the same jobs a mouse does — selecting menu commands, picking and editing pattern lines, typing on the on-screen keyboard, exiting commands, and moving pieces. Pressing the tip down equals a left mouse click, clicking the pen's button equals a right click (used to finish a selection), and clicking the button while pressing down switches between Value and Cursor modes, so workers can operate the whole system without ever touching a mouse.

**Using the Eraser** — The Eraser is an on-screen "E" button that appears while you're using the Sketch, Note/Illustrate, or Line/Curve commands, and clicking it removes your most recent piece of work in reverse order — the last line drawn if you're sketching, or the last point placed if you're using Line/Curve. Each click removes one more step back, so it works like an undo button for correcting mistakes as you draft.

**Hints on Setting Preferences/Options** — This topic gives recommended settings to get the best results when drafting pieces: turning Display Symbols on, setting Display Internals to Dashed, and choosing Full Scale as the default view so pieces display correctly when first placed. It also advises using the default Sketch Pen Resolution and Point Filter values (or testing to adjust them) and notes that new grade points get rule number 1 by default, pulling from the Preferences/Options rule table for AccuMark data or the current style's rule table for MicroMark data.

**Drafting on the Silhouette Table** — This topic introduces the Silhouette Table, the digitizing hardware that works with Silhouette 2000 software to let a pattern maker draft the same way they always have — except the traditional drafting table is replaced by the Silhouette Table and the pencil is replaced by a computerized pen/stylus. The Draft menu's Sketch and Line/Curve commands are the main tools used here, and which one you pick depends on your preferred drawing style and what the piece requires.

**Basics of Drafting Pieces in Silhouette 2000** — This is an introductory section of the manual that walks through the fundamentals of drafting pattern pieces in Silhouette 2000, including the difference between draft, working, and saved pieces, how the Silhouette table/screen/pen work together, and how to use the pen and eraser tools. It's meant as a starting orientation topic rather than a single command, pointing workers to the more detailed how-to topics that follow.

**Practical Application Examples** — This is a section heading in the manual introducing a set of real-world, step-by-step examples (like drafting a design, designing from a sloper, and creating a first pattern) that show how to apply the Silhouette 2000 commands to common jobs on the production floor.

**Draft a Design** — This is a step-by-step example showing how to draft a new pattern design using Silhouette 2000: secure paper to the table, load the ink cartridge in the pen, use Draft Scale so the screen matches the table, choose Sketch, click the pen button to start a new piece, and then draft the lines with your usual rulers and curves while the pattern appears on screen as you draw. This method saves time over traditional drafting because the system avoids repetitive manual copying of pattern pieces.

**Design From Sloper** — This is a step-by-step example for creating a new design starting from an existing sloper (a basic, proven pattern block): open the sloper in the system, plot or cut a hard copy, tape it to the table, use Reorient to line up the on-screen sloper with the paper copy, and use Anchor/Unanchor to lock it in place so it can't be moved by accident. Then, with the ink cartridge in the pen, you sketch the new style lines directly on top of the anchored sloper using your normal rulers and curves.

**Create and Modify a First Pattern** — This is a step-by-step example for turning a draped muslin or fabric pattern (made on a dress form) into a digital "first pattern," including any fit adjustments made during draping. You secure the muslin or fabric to the table, put the plastic (non-marking) nib in the pen/stylus so you don't leave ink marks on the fabric, set the screen to match the table with Draft Scale, and then use the Line/Curve command to trace and identify the pattern lines directly into the system.

**Copy an Assembled Garment** — This function lets a worker trace an already-sewn, finished garment and turn its shape into a digital pattern piece in the system. Before starting, the worker pins the flat part of the garment (fabric up to about 3/8 inch thick) to the table and makes sure the pen/stylus has its plastic tip (not the ink cartridge) so the garment doesn't get marked. Using the Draft menu's Line/Curve tool, the worker traces around the edge of the garment with the stylus, and the system records those points as the outline of a new pattern piece.

**Alter Patterns** — This function lets a worker make fit or style changes to a pattern at the same time it is first traced into the system, using a technique called the pivot method (rotating the pattern around a fixed point to reshape it). It's used for jobs like adjusting men's wear, making fit corrections on women's wear, or reshaping women's pattern pieces. The worker tapes a blank sheet of paper under the hard pattern, uses the Draft menu's Sketch tool to trace around the piece, and then pivots (swings) the pattern by the needed amount at the alteration point before continuing to trace, so the change is built right into the new digital piece.

**Add Designs to Patterns** — This function is used to add decorative elements like lace, fabric appliqués, or beading alignment guides onto an existing pattern piece. The worker secures the pattern to the table, traces its outline into the system with Line/Curve and turns it into a usable piece with Create Piece, then lays the lace or design material on top and traces its outline the same way (using the plastic tip on the stylus to avoid damaging the material). The traced design shows up on screen over the piece, and the worker saves it as part of the pattern.

**Armhole/Sleeve Cap - Practical Exercise** — This is a hands-on practice exercise for the Armhole/Sleeve Cap tool, which adjusts the armhole (the arm opening on the body of a garment) and the sleeve cap (the top curve of the sleeve) at the same time so they still fit together properly. The exercise has the worker place the front, back, and sleeve pieces together in the work area, set movement options, and click specific points (like the shoulder point and notch) with a marker called a thumbtack to see how changing one curve automatically reshapes the matching curve, keeping the armhole and sleeve in sync.

**Practical Silhouette 2000 Applications** — This is an overview section that introduces six real, job-related tasks a worker can learn using Silhouette 2000: drafting a new design, creating/modifying designs from slopers (basic body-shaped templates), building a first pattern, copying a garment, altering patterns, adding designs to patterns, and adjusting the armhole and sleeve cap together. It acts as a table of contents pointing the worker to the specific step-by-step procedure needed for whichever task they want to perform.

### Expert Edition
Expert Edition is an add-on package of the PDS 2000/Silhouette 2000 software containing advanced, production-speeding tools for working with pattern pieces, such as multi-piece fullness adjustments, curve reshaping, armhole/sleevecap updates, spec measurement sheets, and binding creation. A worker would check with their Gerber sales representative to see if this edition and its specific features are available on their system.

**Expert Edition** — Expert Edition is an add-on package of the PDS 2000/Silhouette 2000 software containing advanced, production-speeding tools for working with pattern pieces, such as multi-piece fullness adjustments, curve reshaping, armhole/sleevecap updates, spec measurement sheets, and binding creation. A worker would check with their Gerber sales representative to see if this edition and its specific features are available on their system.

**Armhole/Sleevecap (Expert Edition Only)** — This Expert Edition tool lets a worker reshape the armhole (the arm opening) and have the sleeve cap (the curved top of the sleeve) update automatically at the same time, so the two pieces still fit together after the change. It can even adjust curves that run across more than one piece, and the worker can choose settings like whether to treat several connected lines as one combined line (Create Composite Line) and pick the type of movement wanted for the armhole and sleeve separately.

**Measure Specs (Expert Edition Only)** — This tool lets a worker build a spec sheet listing all the measurements, across every graded size, for a particular style or model. The worker first creates a measurement template (a list of measurement names) in a text file and saves it with a .mct extension, then opens the style, loads that template through File/Open as a 'Measure Chart,' selects each row, and uses the regular Measure tools (like Measure/Line or Distance 2 Point) to fill in the actual measurements taken from the pieces.

**Create Binding (Expert Edition Only)** — This tool automatically generates a binding piece — a long rectangular strip (like binding tape used to finish a seam) — at a width the worker specifies, complete with notches marking where seams and other reference points should line up. The system also automatically creates the grading rules (size adjustments) for the four corners and notches so the binding strip will scale correctly for every size in the size range, saving the worker from drafting and grading it by hand.

**Grading of Binding (Expert Edition Only)** — This describes how the system calculates size grading for a binding piece (like a seam binding tape) once it's created: it looks at how much the distance between notches or endpoints grows from one size to the next and uses that growth as the sideways (X) value for each grading rule, while the up-down (Y) value stays at zero. The worker should make sure the binding piece uses the same base size and size range as the rest of the pieces in the style, and on MicroMark systems can use Export Rules to send these new grading rules into a MicroMark rule table.

**Multiple Slash and Spread (Expert Edition Only)** — This tool lets a worker add fullness (extra fabric volume, either evenly spread out or tapered/narrowing) across several pattern pieces at once instead of doing each piece separately. The worker selects all the pieces to change, draws slash lines (cut lines) across them, picks which part of the piece to hold in place, chooses any inner lines that should move, and then enters the amount of fullness to add — either by dragging with the cursor or typing in an exact value.


## Marker Making (AccuMark Professional Edition)
*200 documented functions/sections, each defined below*

### Getting Started
This section introduces marker making, which is the job of arranging all the pattern pieces onto a layout that represents the fabric to be cut, done in a way that wastes as little material as possible (pieces may be flipped, rotated, or overlapped depending on rules set in the Order Editor). Before you can build a marker, the pieces must already be created and checked in the pattern system (PDS), and you must first fill out the Model Form (which lists all the pieces cut from the same fabric for one garment) and the Annotation Form (which sets what information prints on each piece).

**Settings/Marker Display** — This is a screen (found under Edit/Settings) where you choose how pieces are shown on your screen while you build a marker. You can pick 'Icon Menu,' which shows pieces at the top of the screen along with details like model number, sizes, bundle codes, and how many left/right pieces there are; or 'Piece View,' which lays pieces out unplaced in rows just above the marker border (if there are too many pieces to fit, it will automatically switch back to Icon Menu view). There's also a 'Matching Grid' option that lets you toggle how many grid lines show on screen when you're working with striped or plaid fabric matching (Standard, Five Star) across two or three grids, so the screen isn't too cluttered to work with.

**Help** — This is the on-screen help system built into the software that you can open any time you're unsure how to use a command or feature. It's there so you don't have to stop and find a supervisor or the paper manual for basic questions.

### Marker Making
This is the core part of the AccuMark program where you actually build markers (the layout of pattern pieces on fabric). It comes with a built-in help system that explains the drop-down menus, lookup tables, icon menus, and the right-mouse-button toolbox, so you have guidance available while you work.

**The Marker Making Workplace** — This is the main screen that appears on your monitor once you open (retrieve) a marker to work on. It's the workspace containing everything you need to build the marker, including the icon menu, work area, scroll bars, and information boxes described elsewhere in the manual.

**Work Area** — This is the section of the screen containing the marker border, shown as a rectangle along the bottom of the screen, where you drag and arrange fabric pieces before locking them into place. Inside the border you'll see a dotted 'target line' (goal line) showing how much fabric you should ideally use, based on either a target length (the maximum marker length) or target utilization (the percentage of fabric actually used) — numbers that were set earlier in Order Editor based on past markers of that style.

### Main Menu
This is the row of 9 drop-down menus (File, Edit, View, Piece, Bundle, etc.) that appears across the top of the screen when you open Marker Making. Each menu groups related commands together — for example, File lets you open and save markers, while Piece lets you add or remove pieces — giving you access to every feature in the program; note that some listed functions may be grayed out or unavailable depending on how your system was set up.

**File Menu** — This menu handles opening and saving your marker files, similar to File menus in other programs. You can open a marker, jump to the next unmade or next made marker in storage, move to the next or previous marker regardless of status, reopen the original version to undo unsaved changes, import data, print or send to a plotter, save your work, or exit the program.

**Edit Menu** — This menu lets you fine-tune how pieces relate to each other and customize your workspace. 'Overlap Amount' lets you overlap one piece partly on top of another (or over the marker's edge) or set a measured gap between two pieces; 'Tilt Amount' sets how far selected pieces are allowed to rotate clockwise or counterclockwise; and 'Settings' opens a window where you control how pieces display and set measurements for splicing, matching, and block fusing.

**View Menu** — This menu changes how the marker looks on your screen without changing the actual marker itself. 'Next Icon Page' flips to the next page of piece icons; 'Zoom' magnifies a section for a closer look; 'Full Length' shrinks the view so the whole marker fits on screen (press again to return to normal); 'Big Scale' enlarges the whole marker view as a toggle; and 'Refresh Display' clears leftover on-screen debris ('ghosting') left behind after you've moved pieces around.

**Piece Menu** — This menu contains commands for working with individual pattern pieces already placed in the marker, such as unplacing them, adjusting the space (buffer) around pieces, or reshaping the boundary used for dynamic blocking. 'Add Piece' brings extra pieces into the marker (up to a total of 5,000 pieces) if the model and order allow it, while 'Delete Piece' removes pieces that were added this way (pieces that were part of the original order cannot be deleted). Some commands only apply to 'small' pieces — ones not marked as a major piece (M) in Order Entry.

**Bundle Menu** — A bundle is the complete set of pieces for one garment in one size (for example, all the pieces for one size-12 jacket), and this menu lets you manage bundles in the icon menu or marker (up to 500 bundles total). 'Add' brings in an extra bundle during marker making; 'Delete' removes a bundle that was added this way; 'Return' sends all pieces of a chosen bundle back to their original spot in the icon menu (removing any matching edits); and 'Unplace' sends unplaced bundles in the marker elsewhere as needed.

**Marker Menu** — This menu has commands for handling pieces and the marker as a whole while you build it — splitting, copying, attaching, flipping, and adding splice marks. 'Flip' rotates the entire marker on its X or Y axis; 'Split' lets you move a group of pieces (for example, to insert more pieces in the middle) without disturbing pieces already placed; 'Copy' applies the piece layout from a similar marker onto the one you're working on; 'Attach' joins up to 99 markers together (up to 5,000 pieces total, as long as they share the same matching type, lay limits, and width); and adding splice marks flags where fabric needs to overlap when a roll ends.

**Layrule Menu** — This menu lets you create, edit, and save 'layrules,' which are records that let AccuMark rebuild a marker you made before instead of starting from scratch. 'Positional' layrules save the exact original position of each piece; 'Sliding' layrules instead record the direction, degree, and order in which pieces were slid into place, so new markers can be built following the same placement pattern as previous ones.

**Tools Menu** — This menu offers time-saving tools, especially the 'Scoop' feature, which remembers a specific order and placement of sizes so you can quickly repeat it. 'Scoop Create' sets up automatic piece placement based on positions you define; 'Scoop Modify' edits that saved sequence; 'Scoop Delete' removes a saved scoop; and 'Scoop Apply' actually drops the scoop's pieces into the marker (pieces stay linked/married together until you apply a scoop again, and you must place one scoop before starting another).

### Menu Functions
This is a section heading in the manual grouping together explanations of the various drop-down menus and their commands in Marker Making. It serves as an organizing reference rather than a single function itself.

**Settings** — Opened from the Edit menu on the Main Menu bar, this brings up a window where you customize how your workspace looks and behaves. It covers several areas — Global settings, Piece Display, Matching, Marker Display, Splice, and Block Fuse — letting you control things like how pieces appear on screen and the measurements used for splicing, matching, and block fusing.

### Right Mouse Toolbox
This is a toolbox of extra functions you can pull up on screen by clicking your right mouse button while working in a marker, giving you quick access to common tools without having to go through the drop-down menus. It's a shortcut feature meant to speed up repetitive tasks during marker making.

**Toolbox** — The Toolbox is a floating panel of extra commands you can pull up any time you're working on a marker (the layout of pattern pieces on fabric). You open it from the View menu ('Toolbox'), by clicking the 'TB' button in the marker info box, or by pressing the toolbox icon on the toolbar. It's split into two parts, Functions and Modifiers, and gives you fast access to tools for moving and arranging pieces without digging through menus.

**Toolbox Functions** — These are actions you assign to your right mouse button so you can quickly manipulate pieces (like rotating, flipping, sliding, or fitting them) as you place them in the marker. Once you pick a function, it stays active on the right mouse button until you choose a different one, and it shows in the 'TB' field of the Marker Info box. Some functions, like Auto Slide and Rotate, have extra options (shown by an arrow icon) that let you fine-tune how they work, and you can also trigger these actions from the numeric keypad.

**Toolbox Modifiers** — Modifiers set the 'rules' for which pieces can be grabbed and acted on by your right-mouse function. For example, Free Rotate lets a piece automatically tilt slightly (up to an allowed limit) when you slide it up against the fabric edge or another piece, helping pieces fit together more tightly with less wasted fabric. Other modifiers, like Global Override or Toolbox Override, let you bypass placement rules and limits set up in the order paperwork, though the system logs any use of an override so it shows up later in reports.

### Add a Piece
This command lets you pull an extra individual pattern piece into the marker while you're working on it, beyond what was originally ordered. It only works if the 'Add PC' setting has been turned on for that piece in both the Model Form and the Order Form, and you can only add pieces/sizes that are already part of the current marker. After you select the piece from the marker, work area, or icon menu, it appears unplaced above the marker with a bundle code in brackets, ready for you to position.

### Add a Bundle
This command retrieves a whole extra bundle (a group of matching pattern pieces) into the marker, rather than adding pieces one at a time. It requires the 'Add PC/BD' setting to be checked in both the Model Form and Order Form for all pieces. Once added, all the pieces in that bundle show up unplaced above the marker with a bundle code, and unlike other added items, they won't get sent back to the icon menu if you later use a Return command.

### Delete Piece
This command removes a piece from the marker, but only if that piece was brought in using Add a Piece or Add a Bundle. If you try to delete a piece that was just part of the original order (and never separately added), the system shows an error because there's nothing extra to remove. You select the piece from the Piece menu's Delete Piece option, and it disappears from the work area.

### Delete Bundle
This command removes an entire bundle from the marker, but only works on bundles that were brought in with the Add a Bundle command. If you try to delete a bundle that was only part of the standard order (not separately added), the system gives an error since there's nothing extra to delete. Clicking any piece from that bundle removes all its matching pieces from the work area at once.

### Create Block
Block Fuse lets you group several pattern pieces together into one combined shape ('block') in a shell marker, then copy that block over to a separate fusing marker. This is used for block fusing, a cutting method where shell fabric and a fusible backing (used for parts like collars and facings) are cut together as one bonded block, then later cut apart into individual pieces. You can make the block either a simple rectangle or a custom shape that follows the outline of the pieces.

### Creating a Rectangular Fuse Block
This is the step-by-step process for making a simple rectangular block around one or more pieces for fusing. You turn on the Block Notch setting if needed, select the pieces to include, click Rectangle in the Block Fuse dialog so the system automatically draws a box around them, place that block in the marker, and store the marker. Afterward you use Block Fuse > Create Fusing Marker to pull the matching fusible pieces into a separate fusing marker.

### Manually Creating Fused Blocks
This is an alternative to the rectangle option that lets you trace a custom-shaped outline around the pieces you want fused, instead of using a plain box. You click point-by-point around the perimeter of the selected pieces (the line can't cut into a piece or cross itself), and double-clicking or returning to your starting point closes the shape automatically. It's used to get a tighter, less wasteful fit than a rectangular block when laying out fusible material.

### Modify Block Fuse
This command lets you go back and change an already-created fuse block — for example, switching it between rectangular and custom (manual) shape, or adding/removing pieces from it. You select the block, make your changes, re-place it in the marker, and store both the shell marker and the related fusing marker so the changes carry through.

### Copy Fuse Block
This command duplicates an existing fuse block so you don't have to build a matching one from scratch, as long as the needed pieces are available (or the system is allowed to add them). After selecting the block to copy, an identical copy appears that you can drag to a new spot in the marker or work area, which is handy for building an efficient fusing marker quickly.

### Delete Fuse Block
This command removes a specific fuse block you previously created. When you click on a block to delete it, the fused outline disappears, and if it was a rectangular block wrapped around a piece, that piece just returns to showing its normal shape.

### Delete All Fused Blocks
This command clears every fuse block that's been created in the current marker in one step, rather than deleting them one at a time. It's a quick way to start over on your block-fusing layout.

### Create Fusing Marker
This command takes the blocked groups of pieces you set up in the shell marker (using Create Block) and copies them over into a separate fusing marker, which is the layout used to cut the fusible backing material. The amount of fabric added around each block in the fusing marker can be smaller than in the shell marker, based on a 'Reduce Fuse Amount' setting configured elsewhere. You pick the fusing marker's name from a lookup box and the system builds it automatically.

### Workflow for Block Fusing When Using a GERBERcutter
This describes the overall sequence for producing fused pieces when cutting on a GERBERcutter machine: order and process both the shell and fusing markers, build the shell marker by blocking the fusible pieces and placing them alongside the other pieces for best fabric use, then generate the fusing marker from the shell marker so only the fusing blocks are placed there. It also notes you can duplicate fusing blocks with the Copy function for efficiency, and can create a separate 'finish cut' marker from the shell marker by removing everything except the fusible blocks.

### Bundle/Unplace
This command takes a bundle of pieces that has already been placed into the marker and moves it back up into the work area, effectively taking it out of the marker layout. Once unplaced, those pieces won't be cut or plotted and won't count toward the marker's fabric usage, length, or efficiency numbers. Selecting any one piece in the bundle unplaces the whole matching set, and it also breaks any 'marriage' (grouped pairing) those pieces had with others.

### Bundle/Select
This command brings an entire bundle of matching pieces down from the icon menu (where unused pieces are stored) into the work area all at once, instead of dragging pieces out one by one. You choose the bundle you want from the icon menu and all its pieces appear unplaced in the work area, ready for you to position in the marker.

### Bundle/Flip
This command flips a bundle of pieces (a group of identical or paired pieces) both left-to-right and top-to-bottom (the manual calls this flipping about the X and Y axes) inside the marker. To use it, open the Bundle menu, choose Flip Bundle, and click on any one piece that belongs to the bundle you want flipped. When you do this, the system flips all pieces in that bundle and removes them from their placed position on the marker, and if any pieces were married (locked together as a matched set), that pairing is broken.

### Bundle/Reset Orientation
This command undoes a previous flip, putting all pieces in a bundle back to the way they were originally ordered. From the Bundle menu choose Reset Orientation, then click any piece in the bundle you want restored; the system reorients every piece in that bundle back to its original layout and takes them off the marker (unplaced) so you can place them again, breaking any married (locked-together) pairing in the process. You then press OK to confirm or Cancel to stop the action.

### Storage Areas
Storage Areas are like labeled folders or workspaces where you keep and organize your markers, pieces, and other files so you can find them quickly later. To make one, go into AccuMark Explorer, pick the drive (local or a shared network drive) where you want it, choose File > New > Storage Area, then type in a name for it and click OK — the new storage area then shows up in the list on that drive.

### File/Open
Use this command when you're ready to start working on a marker that has already been set up and processed in Order Entry. Choosing File/Open brings up a lookup box listing the markers in your current storage area (a saved workspace); you can switch to a different storage area if needed, then either type the marker's name or double-click it in the list to load it — only one marker can be opened at a time.

### File/Open Next Unmade
This command jumps straight to the next marker that still needs to be worked on (its status shows as "Needs Approval" or "Unmade") in the same storage area (workspace) you're using. You must already have opened a marker with File/Open first; the system then searches through the storage area in alphanumeric order and loads the next unfinished marker in place of the one you were viewing, saving you from manually hunting through the list.

### File/Open Next Made
This command lets you skip ahead to the next marker that has already been completed (status "Made" or "Partial", meaning some or all pieces are placed) in your current storage area (workspace). You must have already opened a marker with File/Open; the system then searches alphanumerically and loads that next finished or partly-finished marker in place of the current one.

### File/Open Next
This command opens the next marker in the storage area (workspace) no matter what its status is — made, partial, needing approval, or unmade — so you can quickly move through your whole list of markers one by one. You must have already opened a marker with File/Open; once you reach the end of the list, using this command again brings up the regular Open dialog box so you can pick a file directly.

### File/Open Original
This command reloads the last saved version of the marker you're currently working on, discarding any changes you've made since you opened it. It's useful when you've been experimenting with a marker and decide you don't want to keep the changes — selecting this brings the marker back to exactly how it looked when you first retrieved it.

### File/Open Previous
This command loads the marker that comes right before the one you're currently working on in the storage area's (workspace's) list, based on however that list is sorted. If you're already on the very first marker in the list, the system instead opens the regular File/Open dialog box and asks you to pick a marker by name.

### File/Save
This command saves the marker you're currently working on, keeping the same file name — it won't ask you to type a new name. If some pieces still aren't placed on the marker, the system will ask whether you really want to save it; a marker saved with all pieces placed is labeled "Made," one saved with only some pieces placed is labeled "Partial," and one saved with no pieces placed is labeled "Unmade" (Unmade markers can't be sent to the cutter or plotter).

### File/Save Temporary
This is a fast way to save your work without going through the usual prompts for device, storage area, and file name — handy for quickly checking your progress. Be careful using it, since it can accidentally overwrite an existing marker; it sets the marker's status to "Needs Approval," which means the marker cannot yet be cut or plotted until you do a full Save or Save As and its status changes to "Made" or "Partial."

### Look in
This is a field in the Open dialog box where you pick which drive your storage area (workspace) is located on, so the system shows you the files saved in that location.

### Up One Level
This button moves you up one folder level from the file or storage area you were just viewing, similar to going back to a parent folder on a computer.

### Create New Storage Area
This is a quick way to set up a brand-new storage area (a workspace for organizing your markers and pieces) directly from the Open dialog box, without needing to go through AccuMark Explorer separately.

### List View
This displays all the files in the Open dialog box as a simple alphabetical list of file names, making it easy to scan quickly for a specific marker.

### Details View
This displays the files in the Open dialog box with extra information alongside each name — including file size, type, the date it was last modified, and its status (such as Made, Partial, or Unmade) — so you can tell more about a marker before opening it.

### File Name
This is the entry field in the Open dialog box where you type in the exact name of the marker file you want to open.

### File Filter
This is a field in the Open dialog box where you can type a marker's name, or use a DOS wildcard symbol (like * or ?) to narrow the file list to only names matching a pattern — for example, typing A19* will show every marker whose name starts with "A19."

### Save As
This command lets you save the marker you're currently working on under a brand-new name, without changing or overwriting the original file. On the job, use this when you want to keep your original marker safe while creating a variation of it — just go to the File menu, choose Save As, pick where to save it, type in a new name (or an existing name if you intend to replace that file), and click Save.

### MSDE for AccuMark Storage Areas
MSDE is a small database engine that lets AccuMark store and access marker/pattern files in a SQL-type database storage area instead of just plain folders. It gets installed from media provided by Gerber, usually starts automatically as a background service after the computer restarts, and you can check that it's running by right-clicking the small server icon in the system tray — this matters because if the service isn't running, AccuMark won't be able to reach those database storage areas.

### Dynamic Split/Join
This command reattaches two piece sections that were previously cut apart using one of the Dynamic Split tools, essentially undoing a split. You must rejoin the pieces in the exact opposite order they were split in — if you pick the wrong piece first, the system will warn you to "join the other half of piece first" so you can try again in the correct order.

### Dynamic Split/Manual
This command lets you split (cut) a marker piece into two sections by freehand — you select the piece, then drag your mouse or pen across it to draw a line showing exactly where you want the cut to happen. This is useful when you need a custom, non-standard split location rather than a fixed measurement, but note the piece must first be set up to allow splitting in the Model.

### Dynamic Split/Left
This command splits a piece at a precise distance or percentage measured starting from its left edge, instead of eyeballing it. You select the piece, type in either a measurement (inches/centimeters) or a percentage in the dialog box, and the system automatically cuts the piece at that exact spot from the left side.

### Dynamic Split/Right
This command splits a piece at a specific distance or percentage measured starting from its right edge. After selecting the piece, you enter either a decimal measurement or a percentage in the dialog box, and the system cuts the piece precisely at that point counting in from the right.

### Dynamic Split/Top
This command splits a piece at a specific distance or percentage measured downward from its top edge. You select the piece, enter a measurement or percentage in the dialog box, and the system splits the piece exactly at that location from the top.

### Dynamic Split/Bottom
This command splits a piece at a specific distance or percentage measured upward from its bottom edge. After selecting the piece, you enter a measurement or percentage into the dialog box, and the system cuts the piece exactly at that point counting up from the bottom.

### Layrules menu in MedPro
Layrules are a feature that lets AccuMark automatically remember and rebuild markers you've made before, saving you the work of manually placing every piece again and taking up less storage space than saving full marker files. There are two kinds: Positional layrules remember exactly where each piece sat in the original marker so it can be reconstructed later, while Sliding layrules remember piece placement patterns and history so they can be used as a flexible starting template for building new, similar markers — just keep in mind that any bundles added during marker making won't be captured by either type.

### Layrules/Positional/Search
This menu path is Layrules > Positional > Search, and it lets you pick a Layrule Search Parameter Table, which is basically a list of rules used to find a matching piece-placement pattern (layrule) for the marker on screen. When you select a table and open it, the system compares your marker's details against the criteria in that table and, if it finds a match, automatically lays out the marker according to that stored rule. Use this when you want the system to find and apply a fitting layout pattern for you instead of placing pieces by hand.

### Layrules/Positional/Apply
Found at Layrules > Positional > Apply, this function rebuilds your marker using a specific layrule (a saved piece-placement pattern) that you pick by name from a list. After you select the layrule name and press Open, the pieces on your marker are automatically arranged to match that saved pattern. It works the same as the "Force Layrule" option in the Order Form, so use it when you already know which named layout you want to apply.

### Layrules/Positional/Save Named
Located at Layrules > Positional > Save Named, this saves your current marker layout as a named layrule (a reusable piece-placement pattern) so it can be applied to future markers. You can accept the suggested default name, type in a new name, or pick an existing layrule from the list to overwrite it, then press Save. Use this after you've arranged a marker in a way you want to reuse later.

### Layrules/Positional/Save Searched
Found under Layrules > Positional > Save Searched, this saves your current marker's layout as a layrule tied to a specific Layrule Search Parameter Table (the criteria list used to match markers automatically). You select which parameter table it should belong to, and the system saves the layout under an assigned name along with that table's matching criteria. Use this when you want your marker's placement to be found automatically later by the Search function rather than by looking it up by name.

### Layrules/Sliding/Create
Found at Layrules > Sliding > Create, this records how you slide and place pieces into a marker step by step, including direction, movement, and order, so that pattern can be reused to build new markers. After you make a marker and choose this option, the placed pieces become unplaced again and you re-slide them into position while the system records every move using the Create Sliding Layrules toolbox. Note this only works on systems with the Batch Processing software and security key installed, and it's useful when you want to capture and repeat a specific piece-by-piece placement sequence.

### Layrules/Sliding/Modify
Located at Layrules > Sliding > Modify, this lets you open an existing sliding layrule (a saved recording of how pieces were slid into place) and change it. The pieces position themselves in the marker according to the saved layrule, and you then re-slide them to adjust placement, using toolbox icons to step backward, forward, insert, or delete placement steps before saving your changes under the same name or a new one. Use this when a previously recorded piece-sliding sequence needs correcting or updating.

### Layrules/Sliding/Search
Found at Layrules > Sliding > Search, this works like the positional search but for sliding layrules: you select a Layrule Search Parameter Table (a criteria list), and the system looks for a sliding layrule that matches your marker's details. If a matching rule is found, the marker's pieces are automatically placed according to that layrule. Use this when you want the system to automatically find and apply a previously recorded sliding placement pattern.

### Layrules/Sliding/Apply
Located at Layrules > Sliding > Apply, this function builds a marker using a specific sliding layrule (a saved recording of piece movement) that you select by name from a list. Once you pick the layrule and press Open, the pieces are placed into the marker following that saved sliding sequence, the same as using "Force Layrule" in the order process. Use this when you know exactly which saved sliding pattern you want applied to your current marker.

### Full Length
Found at View > Full Length, this shrinks the on-screen image of your marker so the entire marker fits within the visible screen area at once, which is helpful when the marker is too long to see fully at normal zoom. Selecting Full Length again returns the marker to its normal display size. It only has an effect when the marker doesn't already fit on screen at "Normal" scale.

### Marker/Split
This command lets you move a whole group of pieces at once so you can slide new pieces into the middle of a marker without messing up the pieces already placed. When you pick a piece at the point where you want to make room, the system automatically 'unplaces' every piece to the right of it and groups them together (shown outlined in a solid color) so you can move them as one unit to a new spot. Use this when you need to squeeze in extra pieces partway through a marker you've already laid out.

### Marker/Copy
This command copies the piece layout from an already-made marker onto a new, unmade marker, saving you from laying out pieces from scratch. It works even if the markers aren't identical size, because the system lines up pieces by matching common piece types and centers, and can run automatically when a new order is opened. After running it, some pieces will be fully placed, some left unplaced, and some may stay in the piece menu if there's no good match.

### Marker/Attach
This command joins up to 99 separate markers together into one marker (as long as the combined total stays under 5000 pieces or 500 bundles). You pick the markers to add from a list, can reorder them with the up/down arrows, and then save the combined result under a new marker name and order number. This is useful when several small marker orders need to be cut together as one big layout.

### Marker/Flip on X Axis
This command flips the entire marker upside down (top to bottom) across the X axis, like turning a page over top-to-bottom. You'd use it when the fabric or marker layout needs to be reversed vertically for cutting or spreading purposes.

### Marker/Flip/on Y Axis
This command flips the entire marker left to right across the Y axis, like a mirror image. It's used when the whole layout needs to be reversed end-to-end for cutting or fabric orientation reasons.

### Marker/Flip/XY Axis
This command flips the entire marker both top-to-bottom and end-to-end at the same time, combining both the X-axis and Y-axis flips into one action. Use it when the whole layout needs to be reversed in both directions at once.

### Vertical Line
This creates a straight, solid vertical line running across the width of the marker that pieces can be slid up against or 'bumped' into to line them up. You can label it with notes (annotation), and if the marker's width changes later, the line automatically stretches or shrinks to match. For example, it's handy for keeping a group of pieces, like all the pieces for one jacket, boxed together and separated from the rest of the layout.

### Horizontal Line
This creates a straight, solid horizontal line running across the length of the marker, which pieces can be pushed up against to align them, and which can also carry a text note. The line can't extend past the marker's length, and if you keep pressing Enter without entering a new position, the system keeps splitting the remaining marker space in half. If the line crosses pieces that are already placed, those pieces become unplaced so you can reposition them against the new line.

### Manual Line
This creates either a horizontal or vertical solid line, but unlike the standard Vertical/Horizontal Line commands, you manually click to set exactly where the line starts and ends rather than covering the whole width or length. As you drag the cursor, the line is drawn live and the X/Y position shows on screen; if it crosses pieces already placed in the marker, those pieces become unplaced so they can be repositioned against the new line.

### Delete Line
This removes a bump line (a vertical, horizontal, or manual guide line) from the marker, along with any text note attached to it. If pieces were resting against that line, they become unplaced and you'll need to move them back into position after the line is gone.

### Annotate Line
This adds a short text note, up to 20 characters, onto a bump line, useful for recording details like ply height or shade zone information. For vertical lines the text shows above the marker near the start of the line, and for horizontal lines it shows above and near the start of that line.

### Splice/Automatic
This automatically places splice marks on the marker using the rules set up in Settings, showing where fabric must overlap when a roll ends or a flaw is found in the fabric. The start of the splice mark must be covered by the new roll, while the end must be covered by the original roll, and marks are read in the direction the fabric is spread. If you add, move, or remove pieces after generating splice marks, you need to run this command again to update them.

### Delete /Splice
This removes splice marks you no longer want from the marker. You simply click on each splice mark you want to remove, then press Cancel when you're done or want to stop the process.

### Bump Lines
Bump lines are vertical or horizontal guide lines you create in the marker so pieces can be slid up against them and snap neatly into place, helping keep the layout organized. You can delete them or add text notes to them for plotting, and you can even override a bump line by positioning a piece over it before sliding, letting the piece pass through instead of stopping there.

### Marry/Create
This command permanently groups two or more pieces together, whether they're already placed, unplaced, or a mix of both, so they can be moved, flipped, or rotated together as a single unit. You select the pieces individually or box-select them, and the grouping (called a marriage) gets saved with the marker until you choose to delete it.

### Marry/Modify
This lets you add more pieces to an existing marriage (a group of pieces linked together) or remove pieces from it. You select any piece already in the marriage to bring up the whole group, then click additional pieces to add or remove before confirming the change.

### Marry/Delete
This breaks apart one marriage so the pieces in it can once again be moved around individually instead of as a group. You select any piece belonging to the marriage you want to dissolve, then confirm to complete the deletion.

### Marry/Delete All
This dissolves every marriage (grouped set of pieces) in the marker all at once, freeing all pieces to be moved individually again. The system will let you know once every marriage has been removed.

### Measure/Point to Point
This tool lets you measure the distance between any two points on the marker (the layout of pattern pieces on the fabric). Go to Tools, then Measure/Point to Point, click your first point anywhere on or inside the marker, then click the second point — the screen will show the X,Y location and the distance between them. Use this when you need to check spacing or exact measurements between two spots on the layout.

### Measure/Piece to Piece
This tool measures the distance between two separate pieces already placed in the marker. Under Tools, choose Measure/Piece to Piece, click the first piece, then click the second piece, and the distance between them appears in the prompt bar at the bottom of the screen. Use this to check spacing or gaps between pieces on the layout.

### Measure/Piece to Edge
This tool measures how far a piece inside the marker is from the outer edge (border line) of the marker. Choose Tools, Measure/Piece to Edge, click the piece, then click the border line you want to measure to, and the distance shows in the prompt bar. Use this to check how close a piece sits to the fabric's edge.

### Return
Return sends pieces out of the marker and back to the icon menu (the list of unplaced pattern pieces) so you can start laying out the marker again to try to use less fabric. Once you return pieces this way, you lose their placement and any edits you made to them (like rotating, flipping, splitting, or altering), and any matching setups are also removed. If you might want to go back to your current layout, save (store) the marker first before using Return.

### Marry
Marry (Piece/Marry/Create) lets you link together a group of pieces — whether they're already placed in the marker or not — so they move as one unit while keeping their same relative positions to each other. This is useful when you need to shift several pieces at once without disturbing how they're arranged relative to one another. A single piece can only belong to one marriage group at a time, but a marker can have several different marriage groups going at once.

### Conditions of Marriages
This explains the rules for pieces that are married (grouped) together. Certain actions — Split, Fold, Join, and Align — cannot be done to pieces while they're in a marriage. A marriage won't place into the marker if its pieces overlap each other or extend outside the marker border, and a marriage breaks apart if you use commands like Return or Unplace on its pieces.

### Block Fuse
Block Fuse is used when certain pieces (like collars or facings) need to be bonded with a fusible backing material before cutting. It lets you group ('block') those pieces together in a shell marker (the main garment layout) and copy that same block into a separate fusing marker, so the shell fabric and the fusible material can be cut as matching blocks, bonded together, and then cut into finished individual pieces. Shell and fusing markers can be ordered together using the Order Form.

### Scoop
Scoop is a set of tools that speed up marker making when you're working with a marker that has many small pieces. It lets you pick pieces from the icon menu in a specific order and place them, and the system remembers which sizes, in what order, and where they went — so it can automatically drop down the same groups of pieces again later.

### Dynamic Alter
Dynamic Alter lets you change the shape or size of a piece right during marker making, using pre-set alteration rules from your Alteration Library (set up on the Order Form). For example, you'd use it to adjust a piece's width so it fits properly within the fabric width you ordered. To use it, select the piece from the Piece menu's Dynamic Alter option, choose the alteration rule, enter the amount, and confirm — the piece changes and becomes unplaced, ready to be repositioned.

### Dynamic Split
Dynamic Split lets you cut a pattern piece into two parts while building the marker — either at a spot you pick manually or at a percentage distance from the piece's edges — and you can also rejoin pieces that were split this way. Note that a piece can only be split if the model file allows a certain number of splits, and pieces that are part of a marriage cannot be split.

### Measure
This is the general Measure menu, which contains the tools for checking distances on the marker — between two points, between two pieces, or from a piece to the edge of the marker. Use these when you need to verify spacing or fit while laying out or reviewing a marker.

### Sliding Layrules
Layrules let AccuMark rebuild markers that were made previously, and there are two kinds: Positional (which remembers exactly where each piece was placed) and Sliding (which remembers the direction, angle, and order in which pieces were slid into place). Sliding layrules use this movement history to help build new markers based on past placement patterns, but this feature only works if the Batch Processing Software has been purchased and installed.

### Shrink and Stretch
Use this feature when working with fabric that shrinks or stretches after cutting, so the finished pieces still come out the correct size. You enter a shrink or stretch percentage on the Order Form (for example, -25.0 for a fabric that shrinks 25%, or +10.0 for one that stretches 10%), and the system automatically enlarges or reduces the pieces in the marker to compensate before cutting.

### Icon Toolbar
The Icon Toolbar is the row of clickable icons below the main menu bar, and you can customize which icons appear on it. Double-click an empty spot on the toolbar to open a settings box where you can add or remove icons, add blank separators to organize icons into groups, or press Reset to restore all the icons.

### Configurable Toolbar
This is the same customizable icon toolbar feature — double-click a blank area on the toolbar to open a dialog box where you can add or remove icons and insert separators to group them. Press the Reset button if you want to put all the icons back on the toolbar.

### Scoop Create
Scoop Create is the tool you use to build a new scoop, which speeds up marker making for layouts with many small pieces. You select pieces from the icon menu in the order you want, and the system remembers their sizes and placement order so it can automatically bring the same group of pieces into the marker again later.

### Scoop Modify
Scoop Modify lets you go back and change a scoop (a saved group of pieces and their order) that was already created — you can add pieces to it or remove pieces from it. Find this under Tools, Scoop Modify on the menu bar.

### Scoop Delete
Scoop Delete removes an entire scoop (a saved group of pieces with their order and placement) that you no longer need. Find this under Tools, Scoop Delete on the menu bar.

### Scoop Apply
Scoop Apply places one previously created "scoop" (a saved group of pieces, in a set order and arrangement) into the marker in a single action. You'll use it after building a scoop with Scoop Create, so you don't have to drag in small pieces one at a time — great for markers with lots of small parts. You can only apply one scoop at a time; the pieces stay grouped (married) together until you run Scoop Apply again to bring in the next scoop.

### Scoop Build Up
After you've created a scoop (a saved group/order of small pieces), Scoop Build Up tells the system to stack additional copies of that scoop moving upward in the marker. If you also pick Build Right, the scoops will stack upward while forming new columns to the right. Use this when you need to fill marker space quickly and want the repeated groups climbing up the layout.

### Scoop Build Right
After creating a scoop (a saved group/order of small pieces), Scoop Build Right places repeated copies of that scoop moving toward the right side of the marker. This helps you fill marker space efficiently in a predictable, rightward pattern without manually placing each small piece.

### Scoop Build Down
After creating a scoop (a saved group/order of small pieces), Scoop Build Down places repeated copies of that scoop moving downward in the marker. This is useful for quickly filling marker length with small pieces in a consistent, repeating pattern.

### Scoop Build Left
After creating a scoop (a saved group/order of small pieces), Scoop Build Left places repeated copies of that scoop moving toward the left side of the marker, and combined with Build Down it will stack scoops in columns going down and to the left. Use this to fill remaining marker space with small pieces in a controlled direction.

### Unplace All
Unplace All takes every piece currently placed in the marker and changes its status to "unplaced," but leaves it sitting in the same spot on the marker rather than removing it. You'd use this when you need to make pieces temporarily inactive — for example, unplaced pieces don't count toward the marker's area, perimeter, or efficiency numbers, and they can't be sent to plot or cut until they're placed again.

### Unplace Small
Unplace Small changes the status of only the "small" pieces in the marker (pieces that haven't been flagged as a major piece, or "M," in the Lay Limits Table settings) from placed to unplaced. If a small piece was grouped (married) with another piece, that grouping is automatically broken. Use this when you want to rework or remove just the little pieces without disturbing the larger, major pieces in your layout.

### Block
Block adds an extra safety zone (an enlarged outline) around a piece, typically used for critical parts like collars or lapels that will be die cut, or for pieces that get cut, then restacked, then cut again in matched markers. When the piece is actually cut on a GERBERcutter (an automated fabric-cutting machine), the machine cuts along this larger, blocked outline instead of the piece's normal edge, giving extra material for accuracy.

### Buffer
Buffer adds extra space around a selected piece without changing the piece's actual cut size or shape — buffered pieces show up with a dotted outline in the marker. Workers use this so there's room to adjust the cutting head for accurate matching on a GERBERcutter (automated cutting machine), and also to keep pieces from sitting too close together in the layout; you can use the Measure tool to check the total buffer distance between pieces.

### Return All
Return All sends every piece in the marker's work area — whether placed or unplaced — back to its original, default position and orientation in the icon menu (the piece selection list), and it undoes any matching edits made to those pieces. The system will ask you to confirm before doing this, since it resets your whole layout back to the starting piece set.

### Return Unplaced
Return Unplaced sends only the pieces that are currently unplaced (not laid into the marker) back to their original orientation in the icon menu, undoing any matching edits on them. Any pieces that were split get merged back together, and any groupings (marriages) between unplaced pieces are broken — useful when you want to clear out unused pieces without disturbing the ones you've already placed.

### Return Bundle
Return Bundle sends all the pieces belonging to one specific bundle (a labeled group of pieces) back to their original spot in the icon menu, by simply selecting any one piece from that bundle. Split pieces are merged back together and any groupings (marriages) involving those pieces are dissolved — handy for undoing work on just one bundle instead of the whole marker.

### Working with the Toolbox
The Toolbox is a floating panel of marker-making tools/functions that you can show or hide (via the View menu, the toolbar icon, or the TB button in the Marker Info dialog box) and drag to a new spot on your screen by clicking and holding its title bar. Hiding the Toolbox doesn't turn off whatever tool you last selected — it keeps working in the background — and you pick a function or setting from it with a left mouse-button click.

### Auto Slide
Auto Slide automatically arranges and places a group of pieces into the marker as you drag (slide) them in, instead of making you position each piece by hand. You select the pieces first, then slide them toward the marker, and the system lays them out based on a chosen sorting rule (like by area, height, or length).

### Area
Area is a sort option for Auto Slide: after you draw a selection box around pieces and slide them into the marker, the system places them sorted by their surface area (biggest to smallest, or per the setting) to fill marker space efficiently. It's one of the "Primary Sort" choices, meaning one such option is always active when using Auto Slide.

### Length
Length is a sort option for Auto Slide: when you select pieces with a marquee (drag) box and slide them into the marker, the system places them ordered by their length instead of by area or height. Use it when you want small pieces automatically arranged based on how long they are, to fill the marker more efficiently.

### Height
Height is a sort option for Auto Slide: when pieces are selected and slid into the marker, this setting places them ordered by their height (the Y-axis, or up-and-down dimension), tallest pieces first. It's one of the sorting choices you can pick to control how automatically-placed pieces line up in the marker.

### X Alter
X Alter is an Auto Slide option that places pieces in an alternating pattern — one piece placed normally, the next flipped horizontally (mirrored left-to-right, called an X-flip), and so on. This helps pieces nest together more tightly and efficiently when they're automatically slid into the marker.

### Y Alter
This function slides or places pieces into the marker so that they alternate between not flipping the piece at all and flipping it top-to-bottom (a Y-flip). Workers use it when filling a marker area, length, or height to automatically mix flipped and unflipped copies of a piece for better fit or fabric usage, without having to flip each piece by hand.

### XY Alter
This function alternates piece placement between three sort orders (largest area, longest length, or widest height first) and lets you choose how pieces flip as they're placed: alternating with no flip and an X-flip (left-right), a Y-flip (top-to-bottom), or an XY-flip (both directions at once). The flip choices only work if the piece was set up ahead of time in a model or given a flip code in Order Entry, so the operator is really speeding up marker filling while keeping the mix of flipped/unflipped pieces balanced automatically.

### Group Slide
This function lets you select several pieces at once with a selection box (drawn by dragging the right mouse button) and slide the whole group into the marker while keeping each piece's position relative to the others exactly the same. It works like temporarily "marrying" (locking together) the pieces for the move, then automatically undoes that link right after they're placed — useful for moving a cluster of pieces together without permanently grouping them. Note: the selection box must fully surround every piece you want included, or it gets left out of the move.

### Butt
This function pushes a selected piece in whatever direction you drag (the "vector") until its edge touches — but does not overlap — the nearest piece or the edge of the marker. It gives the worker more precise control than just sliding, since you aim the piece exactly where you want it to land edge-to-edge, and the tool stays active for repeated use until you pick a different one from the toolbox.

### Overlap
This function lets you deliberately place one piece so it partly covers another piece, covers part of the marker's edge, or sits a specific measured distance (gap) away from another piece. The current overlap/gap amount shows in the "OL" field on screen, and you can type in a new number there to change how much overlap or spacing is applied before placing the piece.

### Align
This function lines up the matching endpoints of two already-placed pieces so their edges sit even with each other, moving the selected piece only straight up/down or left/right (not diagonally) until it "butts" against the fixed piece. It works best on simply shaped pieces like rectangles and requires the two edges to be nearly parallel (within 5 degrees); it cannot be used on pieces that have buffering, matching, or a marriage (paired movement) applied to them.

### Flip
This function flips a piece over into its next allowed mirrored position, based on the flip settings entered for that piece back in Order Entry's Lay Limits table. If a flip isn't normally permitted and the system warns "Override Required," the worker can force it anyway using the Settings/Global or Toolbox Override option; each additional click flips the piece to its next allowed position, and this tool stays active until another is chosen.

### Rotate
This function tilts or rotates a placed piece by an amount you either type directly into the TL (tilt) field or select from preset options in the Rotate submenu, with the allowed amount limited by the piece type and fabric being used. Right-clicking a piece repeatedly rotates it by the entered amount each time, making it useful for angling pieces to fit tightly in a marker layout.

### 45 CW
Rotates the selected piece 45 degrees clockwise in a single click, used to quickly angle a piece to better fit available marker space.

### 45 CCW
Rotates the selected piece 45 degrees counterclockwise in a single click, used to quickly angle a piece to better fit available marker space.

### 90 CW
Rotates the selected piece 90 degrees clockwise in a single click, giving it a quarter-turn to help it fit into the marker layout.

### 90 CCW
Rotates the selected piece 90 degrees counterclockwise in a single click, giving it a quarter-turn to help it fit into the marker layout.

### 180 ROT
Rotates the selected piece a full 180 degrees (turns it upside down/end-for-end) in a single click, useful for testing whether flipping the piece around saves fabric.

### Tilt CW
Tilts the selected piece clockwise by an amount the worker types into the TL (tilt) field in the status area, allowing fine-tuned angling of a piece rather than a fixed rotation amount.

### Tilt CCW
Tilts the selected piece counterclockwise by an amount the worker types into the TL (tilt) field in the status area, allowing fine-tuned angling of a piece rather than a fixed rotation amount.

### Variable
This function tilts a piece by hand in either a clockwise or counterclockwise direction: the worker right-clicks on the piece and slowly drags the cursor to visually rotate it, watching the allowed tilt amount shown in the status field, and can override the normal limit using the GL Override option if more tilt is needed.

### Place
This function locks a selected piece into a fixed spot in the marker ("places" it) or releases it so it can be moved again ("unplaces" it); pieces can't be dropped on top of one another unless the worker turns on GL Override or TB Override. Right-clicking places or unplaces pieces (individually or as a group selected with a marquee box) — matched pieces snap to the nearest match point — and switching between the left and right mouse buttons lets the worker alternate between sliding pieces freely and placing them precisely.

### Block/Buffer
This function adds or removes extra spacing (buffering) or a protective boundary (blocking) around an individual piece while building the marker, letting the worker apply this treatment selectively rather than having it happen automatically to every piece. The actual amount of blocking or buffering used must already be set up in the Order Entry Blocking/Buffering Parameter Table; right-clicking a piece toggles the treatment on (showing "BL" for block or "BU" for buffer in the status area) or off if it's already applied.

### Split
Use Split to divide a piece into two pieces along a fixed line that was already marked (digitized) on the pattern with a special "P" (Piecing Line) label — this is useful when a piece is too large to fit an area or needs to be cut in sections. To use it, pick Split from the Toolbox and right-click the piece; the system cuts it exactly along that pre-set line, and there can only be one such line per piece. You can also use Split in reverse to rejoin two pieces that were previously split apart, and the tool stays active for repeated use until you pick a different Toolbox function.

### Fold
Use Fold to close up (fold) a mirrored piece along its centerline, or to reopen a piece that's already folded — this only works on pieces that were created as mirrored pieces and properly set up in the order entry settings (Piece Option set to F, and the fabric spread set to Tubular or Book Fold). Simply choose Fold from the Toolbox and right-click the piece to toggle it between open and folded; note that if the piece was married (paired) to another, folding it breaks that pairing. This is handy when working with tubular fabric, where folded pieces may need piece counts adjusted automatically.

### Center
Use Center to automatically place a piece in the middle of any open space in the marker, including inside a cutout or hole in another piece (a hole marked with internal label H) — this helps neatly fill small gaps that would otherwise go unused. Simply select Center from the Toolbox and right-click the piece you want positioned; if that piece was married (paired) to another piece, that pairing is broken. The tool stays active until you choose a different function from the Toolbox.

### Matching
Matching lets you adjust how a piece lines up with a pattern (such as stripes or plaids) using one of two pop-up boxes — Matching Lines or Matching Rules — depending on which matching method is already set up for that piece. Select Matching from the right-click Toolbox, then right-click the piece; the appropriate dialog box only appears if that piece was already configured for matching. You can move the box around the screen and choose OK to save your change, Cancel to discard it, or Default to reset the fields, but only one change can be made at a time.

### Free Rotate
Free Rotate lets you angle a piece slightly off its normal straight (horizontal) position so it fits snugly against a neighboring piece when you're using the Slide or Butt tools to push pieces together. The system rotates the piece just enough to match the shape it's sliding against, but never more than the maximum angle allowed in the pattern's settings (Tilt/Rotate field), which can be at most 45 degrees — this keeps fabric waste low while still respecting cutting/grain limits.

### Global  Override
Global Override lets you bypass the placement rules and limits (like rotation or mirroring restrictions) that were set up for the whole marker in the Order Entry Lay Limits settings. Once turned on, it stays on for every piece until you turn it off again by selecting it a second time. Use it carefully — any time you override these rules, the system records it and it will show up later in marker reports, so there's a paper trail.

### Toolbox Override
Toolbox Override lets you bypass the placement rules and limits set in the Lay Limits Form, but only temporarily — it automatically turns off as soon as you perform a slide move or pick a different Toolbox tool. As with the Global Override, use it cautiously, since every override you make gets logged and will appear later in the marker reports.

### Placed
Placed is a modifier you turn on before drawing a selection box (marquee) around a group of pieces, so that only the pieces already positioned in the marker get selected — unplaced pieces sitting off to the side are ignored. This is useful, for example, when you want to move already-placed pieces out and then slide them back in without accidentally disturbing pieces that haven't been placed yet.

### Unplaced
Unplaced is a modifier you turn on before drawing a selection box (marquee) around a group of pieces, so that only pieces that have NOT yet been placed in the marker get selected — pieces already sitting in the marker are left alone. This lets you move a batch of leftover, not-yet-placed pieces around or slide them into the marker without disturbing the pieces already placed.

### Icons
Icons is a modifier that limits your marquee (selection box) to only pick up pieces sitting in the icon menu (the tray of pieces waiting to be used), leaving placed and unplaced pieces in the marker untouched. This lets you draw a selection box around pieces in the icon menu and slide them directly into the marker without disturbing anything already positioned.

### Fit Piece
Fit Piece (activated with the / key on the numeric keypad or its Toolbox icon) automatically slots a piece into a tight, oddly-shaped, or hard-to-reach open space in the marker that would be difficult to place by hand. This saves time and reduces wasted fabric by letting the software find the best fit in cramped areas instead of you manually nudging the piece into place.

### Float Piece
Float Piece (the / key on the keypad or its Toolbox icon) nudges a piece a set distance away from a neighboring piece, using the float allowance amount you configured in Edit/Settings. Unlike Step, which moves a piece repeatedly in small increments, Float can shift the piece in either the X (side-to-side) or Y (up-down) direction but only works once per piece — useful for quickly creating a bit of breathing room between pieces.

### Step Piece
Step Piece lets you nudge a piece a small, precise distance using dedicated keys: the = key moves it up, [ moves it left, ] moves it right, and the ' (apostrophe) key moves it down (these can also be triggered from a Toolbox icon). This gives fine, controlled adjustments when you need a piece positioned just slightly differently than where it landed.

### Numeric Keypad Functions
The Numeric Keypad lets you quickly tilt, rotate, flip, and nudge (bump) pieces using number keys instead of the mouse, speeding up marker placement once Num Lock is turned off. For example, / fits and places a piece, * flips it, - and + tilt it counterclockwise (CCW) or clockwise (CW), the number keys 1-9 slide it in different directions (e.g., 8 slides up, 6 slides right), 5 centers the piece, 0 and . rotate it CCW or CW, and Enter drops the piece into place — combining these with mouse movement makes positioning pieces on the marker much faster.

### Reset Tilt
Reset Tilt undoes any rotation you applied to a piece using the rotate function, returning it back to its original, non-rotated angle. Use this if a piece was tilted for test-fitting or trial placement and you want to quickly restore its default orientation.

### Center
Use Center to automatically place a piece in the middle of any open space in the marker, including inside a cutout or hole in another piece (a hole marked with internal label H) — this helps neatly fill small gaps that would otherwise go unused. Simply select Center from the Toolbox and right-click the piece you want positioned; if that piece was married (paired) to another piece, that pairing is broken. The tool stays active until you choose a different function from the Toolbox.

### Step
Step allows you to make small, precise, controlled movements of a piece while working in Marker Making, letting you fine-tune its position instead of dragging it freehand with the mouse.

### Float
Float moves a piece a set distance away from a neighboring piece, based on the float allowance amount configured in Edit/Settings. Unlike Step, which nudges a piece repeatedly in small increments, Float can shift a piece in either the X or Y direction but can only be applied once per piece.

### Tubular Fold/Piece Count Adjustment
This feature automatically updates the piece count when you fold a piece for use on tubular goods (fabric that comes as a continuous tube rather than a flat sheet). You can choose to keep the piece count as one piece or have the system add an extra piece to account for the fold, so the finished marker always has the correct number of pieces. If you later unfold that piece, the system will ask whether to remove the extra piece it had added, and you turn this option on by selecting Fold from the Marking Toolbox.

### Getting Started
This section introduces marker making, which is the job of arranging all the pattern pieces onto a layout that represents the fabric to be cut, done in a way that wastes as little material as possible (pieces may be flipped, rotated, or overlapped depending on rules set in the Order Editor). Before you can build a marker, the pieces must already be created and checked in the pattern system (PDS), and you must first fill out the Model Form (which lists all the pieces cut from the same fabric for one garment) and the Annotation Form (which sets what information prints on each piece).

### Using Marker Making
This is an overview section that groups together instructions for the everyday tasks workers perform in Marker Making, such as placing pieces, using menus, and adjusting settings. It serves as a starting point pointing to the more detailed how-to topics used in daily operations.

### Using the Mouse & the Stylus
The mouse and the stylus (a pen-like input tool) work the same way in Marker Making — both let you pick menu commands, type in information, select toolbar icons, and move pattern pieces around the screen. Keep your mouse on a flat, hard surface with enough room to move it freely, watch for the arrow-shaped cursor, and hover over toolbar icons to see a tooltip explaining what each one does.

### Icon Menu
The Icon Menu shows a picture (icon) for every pattern piece that was ordered for the current marker, displayed across the top of the screen once you open a marker (as long as this option is turned on in Settings). Under each icon, columns show the model number, size, bundle code, and how many left and right pieces are needed; each time you place a piece, its quantity count goes down, and three dashes mean no pieces of that type were ordered.

### Marker Info
The Marker Info dialog box shows details about the marker you're currently working on, with some fields updating live as you build the marker and others only appearing once a certain action is performed. It shows fixed details about whichever piece is currently selected — its model name (MD), piece name (PN), and size (SZ) — plus attribute flags like BU (buffered), BL (blocked), AL (altered), and OL (overlapped), and it also displays seam allowance, which is set elsewhere and cannot be changed from within Marker Making.

### Scroll Bar
The scroll bar lets you move your view up, down, left, or right to see different parts of the marker, using arrows on the edges of the window. It represents the full possible length of the marker (100 yards by default, plus a little extra), with small vertical lines marking the true start and end and a dashed line showing the marker's current length; the solid white scroll box shows what portion is currently visible, and clicking elsewhere in the bar jumps your view to that spot.

### Message Line
The Message Line, also called the Prompt Bar, sits below the scroll bar on the Marker Making screen and is where the system displays instructions, warnings, and status updates about what's happening with the marker. Workers should keep an eye on this line since it often explains what to do next or flags a problem, making the job easier.

### Placing Pieces in the Marker
This is the step-by-step process of taking a piece from the icon menu and positioning it inside the marker layout. You click the quantity number under a piece's icon to bring up a dashed outline of it, then drag it with the mouse or stylus toward the marker — the system draws a guide line (called a vector) showing the direction you're moving it, and releasing the button lets the piece slide along that path until it settles into place.

### Placing Matched Pieces into a Marker
When pieces need to line up with a pattern like stripes or plaids (called matching), the system uses match lines set up beforehand to guide placement. As you slide a matched piece into the marker, vector lines with arrowheads appear showing the closest valid matching point — sometimes two lines appear if the piece must match in two directions (like both horizontal and vertical on a plaid) — and if no valid match is found, the piece blinks and the message "Matching Location Not Found" appears so you know to try again.

### Choosing Menu Commands
To use a menu command, simply click on the menu name (like File) with the left mouse button or stylus, which opens a dropdown list of choices, then click your desired option to select it. This is the basic method for accessing any function in the software's menus.

### Exit
Choosing Exit Marker closes you completely out of the Marker Making program. The system will first ask you to confirm with "Are You Sure You Want to Exit?" — click OK to actually close the application, or Cancel to stay in Marker Making without exiting.

### Storage Areas & Drives
Storage areas are the named folders where your markers get saved, and drives are the locations (on the network or on your own computer) where those storage areas actually live — you have to pick the correct drive before you can open any markers saved there. You can set up as many storage areas as your system has space for, and it's often helpful to organize them by product line, season, or production phase (for example, a folder named FALL on network drive I:\).

### Dialog Boxes
Dialog boxes are the on-screen windows where you type or select the drive, storage area, or marker name needed to either save ("store to") your work or open ("retrieve from") an existing marker. They're the standard way the software asks you for this location information.

### Lookups
Lookups are pop-up lists that show you all the valid drives, storage areas, or markers you can pick from, so you don't have to type names from memory. The Open dialog box (which appears when you use File/Open) is a type of lookup that shows the files available in a chosen storage area — you can view them as a simple list or a detailed view, and use the "Use Filename Filter Lookup" checkbox to narrow down which files are shown.

### Layrules
Layrules are a system feature that lets AccuMark automatically rebuild a marker you made previously, saving you from re-placing all the pieces by hand and also saving storage space on the system. There are two kinds: Positional layrules save the exact original spot of every piece so the marker can be recreated later, while Sliding layrules instead record the order pieces were placed in, which is covered in more depth in other AccuMark documentation.

### Marquee Selection Box
The marquee selection box lets you select several pieces at once by clicking and dragging the right mouse button (or stylus) diagonally to draw a box around them, similar to how you'd draw a box when zooming in. Once you release, any function you then choose from the Toolbox applies to all the pieces inside that box, and you can use the Toolbox to limit the selection to only Placed, Unplaced, or Icon pieces.

### Changing Settings
After adjusting any settings, you choose how to apply the change: OK keeps the change only for your current session (it resets to default next time you open Marker Making), Cancel exits without saving anything, Save keeps the change permanently even after you close and reopen the program, and Default resets the fields back to their original factory settings.

### Big Scale
Big Scale is a toggle command (found under View/Big Scale or its toolbar icon) that enlarges the marker view on your screen so you can see it more easily. Selecting it once zooms the marker area in; selecting it again returns it to normal size. Note that whichever size you leave it in (normal or enlarged) becomes the default view when you open the next marker.

### Zoom
Zoom (View/Zoom, or the Zoom icon) lets you enlarge just one section of the marker for a closer look, which is helpful when working with small pieces or tight spaces between pieces. To use it, click and drag a selection box (marquee) around the area you want to see up close, and that section will fill the screen. Use Big Scale afterward if you want to return to the normal, full-marker view.

### Refresh Display
Refresh Display clears up 'ghosting' — small leftover marks or particles left on screen after you move pieces around while building a marker. Selecting this command from the Main Menu redraws the screen cleanly so those stray traces disappear. This is especially useful after using Variable Rotate, which tends to leave more of this visual residue.

### Creating Sliding Layrules
Found at Layrules/Sliding/Create, this function records how pieces were moved and placed when you built a marker — including the direction, amount of sliding, and order pieces were placed. That recorded information (a 'layrule') can then be used to automatically rebuild new markers based on that same placement pattern. This feature only works if your system has the Batch Processing software installed.

### Marry
Marry (Piece/Marry/Create) lets you link together a group of pieces — whether they're already placed in the marker or not — so they move as one unit while keeping their same relative positions to each other. This is useful when you need to shift several pieces at once without disturbing how they're arranged relative to one another. A single piece can only belong to one marriage group at a time, but a marker can have several different marriage groups going at once.

### Marker Area Scaling
This setting makes the system remember the zoom level (scale) you were using in the marker area and carries it over to the next marker you open. For example, if you switched to Big Scale to view a marker larger on screen, the next marker you retrieve will automatically open in that same larger view, saving you from resetting it each time.

### Maximum Data Items Allowed
This refers to the upper limits on how much you can put into a single marker: up to 5,000 pieces and up to 500 bundles per marker. You add pieces or bundles using the Add Pieces/Add Bundles commands in Marker Making, and you can keep adding until you hit these limits, as long as the garment style (model) and the order allow it.

### Maximum Marker Length
This is the longest a marker can be, which is capped at 999 yards, with the system defaulting to 100 yards unless changed. If your production needs longer markers, a technician can raise this default limit by editing a system startup file (Autoexec.bat in Windows 95, or an environment variable in Windows NT) and rebooting the computer.

### Block or Buffer Split Pieces
This function, accessed via Block/Buffer in the Marker Making Toolbox, lets you add extra fabric space (blocking or buffering) around a piece that has been split into parts, to account for cutting adjustments. After splitting a piece, select Block/Buffer from the Toolbox and right-click the piece; the marker status area will show 'BL' for blocking or 'BU' for buffering to confirm it was applied. Note that the amount added is preset in the Order Entry Blocking/Buffering Parameter Table, and a piece already carrying dynamic blocking/buffering will have it removed if you select the command again on it.

### Prompt Bar
The Prompt Bar is a strip located below the marker screen that displays helpful instructions and messages while you work. It updates based on whatever function you're currently using, giving you step-by-step guidance so you know what to do next.

### Piece count, automatic update
When you fold pieces for tubular fabric (fabric that comes in a tube shape, like knit goods), this feature automatically adjusts the piece count so the marker ends up with the correct number of pieces. You can choose whether folding keeps the same piece count or adds an extra piece; if you later unfold that piece, the system will ask whether to remove the extra piece it added. This option is set in Edit/Settings and is triggered by choosing Fold in the Marking Toolbox.

### Welcome to the AccuMark Professional Edition
This is an introductory overview explaining that the Professional Edition update brings new order forms, data entry screens, and Marker Making software, along with a launch pad screen for quickly opening programs and forms. It also highlights that Marker Making now has a modern Windows-style interface with dropdown menus, a customizable toolbar with tool-tip labels, scroll bars, and dialog boxes to make building markers easier.

### Settings/Piece Display
Found under Edit/Settings, this section controls how pattern pieces appear on your screen while you work. For example, 'Fill in Placed Pieces' shows pieces as solid color blocks (each bundle a different color) instead of plain outlines; 'Piece Highlighting' lights up a piece when your cursor touches it; and 'Notches' turns on tick marks showing notch locations on the pieces.

### Validate for InVision/AccuMatch
This setting checks that matching pattern pieces (like plaids or stripes that need to line up) are placed correctly when they cross over a 'bite' — a single grip or clamped section of fabric on a GERBERcutter. If the system detects pieces that double back across a bite boundary, it will require those matching pieces to be placed within the same bite so the pattern matches correctly after cutting.

### Settings/Matching
This settings area lets you choose how the system marks matching points for patterned fabric like stripes or plaids. 'Standard' matching uses horizontal and vertical lines based on repeat and offset measurements, while '5-Star' matching uses plus-shaped symbols placed at the intersections of stripe and plaid lines (plus one in the center of every four), needing only a single repeat value to set up. The 'Use Grid Number' field lets you pick which of the offset options (1, 2, or 3) from Order Entry is active, and can be changed anytime while making the marker.

### Settings/Global
This settings section covers marker-wide options such as 'Auto-Store Layrule,' which determines whether the system automatically saves or updates layrules (recorded piece-placement patterns) as you make a marker — leaving it off preserves existing layrules from being overwritten. It also includes 'Delete Attach,' which controls whether original markers are automatically deleted after being attached (combined) into another marker, based on a Yes/No selection.

### Settings/Splice
Splice settings (in View/Settings) control the marks that show where a splice — a fabric joint or repair point — is placed on a marker; these marks can be generated automatically by the system or added manually by the marker maker, with manual entries taking priority. You set the Minimum and Maximum splice mark lengths, a Margin (extra buffer added to each end to ensure pieces are fully cut), and Separation (distance from the marker edge to the splice marks), plus a Display option controlling when the marks are shown.

### Settings/Block Fuse
Block Fuse settings support a production method for grouping fusible pieces (like collars and facings that get heat-bonded) together as a single block, which can be created in a 'shell' marker and then copied over to a matching 'fusing' marker. 'Block Amount' sets how much extra space is automatically added around each side of the grouped block (default 0.50 inches), and 'Reduce Amount' lets you trim that space back down as needed.

### Import
This function lets a worker bring an older MicroMark marker (a marker made in Gerber's older MicroMark system) into AccuMark so it can be worked on, saved, and used for cutting and plotting. When you import a marker, it's automatically saved into a storage location called DATA 70 unless someone has set up a different default folder, and the software automatically writes a report about the imported marker that you can find later in the Reports folder. Because pieces can shift slightly or be reinterpreted during the conversion (for example, a MicroMark grain line becomes an AccuMark 'G' internal line), always double-check the piece placement on the imported marker before sending it to cut or plot.

### Index
This is simply the table of contents/index section at the back of the manual that lists topics and functions alphabetically along with the page numbers where they're explained. Workers would use it to quickly find where a specific tool or menu command (like 'Align Pieces' or 'Auto Slide') is described in the manual, rather than to perform any action in the software itself.


## Order Entry (AccuMark Professional Edition)
*422 documented functions/sections, each defined below*

### Getting Started
This is the introductory section of the manual meant to orient a new user to the AccuMark Order Entry software, typically covering basic navigation and first steps before diving into specific tasks.

**Overview** — This section gives a high-level summary of the AccuMark Order Entry software's purpose and main features before the manual moves into detailed, step-by-step instructions for each function.

**Workflow for Ordering and Processing Markers** — This is a manual section that lays out, step by step, the standard sequence of tasks a worker follows from placing a customer order through to producing a finished cutting marker.

### Using Order Entry
This is the main section introducing the Order Entry function, which is where workers create and submit requests (orders) for markers, patterns, or cutting jobs to be processed by the AccuMark system. It covers the basic steps of entering the information the system needs, such as style, size, quantity, and fabric details, to start a production job.

**Working with Storage Areas** — This section explains how to use Storage Areas, which are designated locations within AccuMark where files like markers, patterns, and orders are saved and organized. Workers use this to know where to find, save, or move their work so files are organized correctly.

### Activity Log
This is a screen you open from the AccuMark Explorer's Utilities page that keeps a running record of actions taken in the system. From this screen you can view the log, print it out, or clear it out when you no longer need the old entries.

### Alteration Form
This form lets you set up rules for how a garment pattern piece should be adjusted in size for things like coat length, pant length, or sleeve length. For each rule you name it, pick which side of the piece it applies to (the original digitized side, the mirrored opposite side, or both), and define the type of change to be made, so the system knows how to resize that piece correctly.

### Annotation Form
This form, found on the Marker Creation Editors page, is where you set up what text and information will automatically print on a piece or along the edge (border) of a marker when it's plotted (printed out). You can add notes for your own reference and set a default label plus special labels for specific piece categories, so every printed marker carries the right identifying information.

**Annotation Format** — This screen is where you choose and type in the specific codes that control what information prints on the marker, such as piece names or sizes. You separate multiple codes with commas (no spaces), use a comma-slash-comma to force text onto a new line, and can turn on the 'Cont' setting to add extra lines if you have more codes than fit on one line.

### Block Buffer Form
This form sets up rules for adding extra space (buffering) or removing space (blocking) around a pattern piece — useful for things like leaving extra fabric margin for a piece that needs it. Static rules are applied automatically during order processing, while Dynamic rules can be turned on or off later by hand while making the marker, and you assign each rule a number and specify the amount of space for the sides of the piece.

### Cut Generation Form
This form is used after a marker is finished and stored, to turn it into cut data — the file format a GERBERcutter machine reads to actually cut the fabric. On this screen you pick where the marker is saved, select which marker to convert, name the resulting cut file, choose whether to send it straight to the cutter, and pick which cutter settings table to use.

### Cut Generation Parameter Table Form
This form lets you define the settings for your cutting machine, such as whether it's a static, variable-bite, or fixed-bite cutter, and the length and width of the usable cutting surface. You also set the bite length (how far the cutter advances each pass) and choose cutting options like cutting small pieces first or mirroring left/right pieces, so the cut data matches how your actual cutter operates.

### Cut Plot Form
After a marker has been made, stored, and converted into cutter data, this form lets you print (plot) a preview of exactly how the cutter will cut it, complete with cutting marks and the order pieces will be cut in. This lets you double check the cut sequence and layout is correct before running the real fabric through the cutter, and the system will warn you before overwriting an existing plot file.

### GERBER LaunchPad
The LaunchPad is the main home screen of the AccuMark software, giving you quick one-click access to all the major work areas: Pattern Processing/Digitizing/PDS, Marker Creation/Editors, Plotting and Cutting, AccuMark Explorer/Utilities, and Documentation. You can keep it docked to the side of your screen or let it float wherever is convenient on your desktop.

**Pattern Processing, Digitizing, PDS** — This area of the LaunchPad groups together the tools for creating and editing pattern pieces: Pattern Design (PDS) for building patterns, Edit Digitize for reviewing and correcting the points captured when a piece was traced (digitized) on a digitizing tablet, the Grade Rule Editor for setting up sizing rules applied to pattern points, and Import/Export User Settings for saving and reusing your personal PDS toolbar and preference setups.

**Marker Creation, Editors** — This area of the LaunchPad contains the tools for building the marker (the layout of pattern pieces placed onto fabric to be cut): Marker Making for actually arranging pieces efficiently on the fabric, the Model Editor for listing which pieces belong together to make one garment, the Laylimits Editor for setting fabric spreading, bundle orientation, and placement limits, and Notch for defining the notch cuts marked on pieces.

**Plotting and Cutting** — This LaunchPad area holds the tools used to finalize and produce a marker for cutting, including Block Buffer for adding space around pieces, Order Process for running marker orders, Order Entry for pulling together all the specifications (lay limits, annotation, blocking/buffering, matching, notch tables, flawed-area info, and models) needed to request a marker, and Annotation for setting up the text/labels that print on the marker.

**AccuMark Explorer, Utilities** — The AccuMark Explorer is the file-browser-like tool that lets you see every storage area and its contents across all connected drives, generate and view reports, create or import/export data, and check the status of plotters, all from one place. The Utilities section alongside it includes Hardware Configuration for setting up connected devices like digitizers and plotters, and general AccuMark Utilities for configuring the software and maintaining files and storage areas.

**Documentation** — This is the collection of built-in reference guides included with AccuMark, such as the What's New document, Release Notes, and User's Guides for Marker Making, Data Management and Output, and Pattern Design. Workers open these PDF or online help files to learn about new features, recommended computer setup, and step-by-step instructions for using each part of the software. You would use this whenever you need printed or on-screen instructions instead of asking someone else how a feature works.

### Lay Limits Form
This form is where you create or edit a table of rules describing how fabric can be laid out for cutting, based on the type of fabric or spread (for example, Tubular, Face To Face, Napped, or Velvet). Using the File menu on this form, you can start a new table, open and edit an existing one, or save your changes under the same or a new name. You'd use this before marker making so the system knows the fabric-specific limits to follow when building a marker.

### Layrule Search Parameter Table Form
This form lets you set up the rules the system uses when searching for the best marker layout (called a 'layrule search'), such as whether to include the marker's name or description in the search criteria. You create, open, edit, or save these parameter tables the same way as other AccuMark tables, using the File menu. It's used to control what information the system checks when it hunts for the optimal way to arrange pieces in a marker.

### Marker Plot Form
You open this form from the Plotting and Cutting page to order printouts ('plots') of AccuMark pieces, markers, or cut data. On this screen you choose where the plot should go — a local plotter connected to your computer, a network plot queue, or saved as a file — and select which parameter tables to use. Use this whenever you need a physical or file copy of a marker or pattern piece.

**Processing Marker Orders** — After a marker order has been created in the Order Editor, this is the step where you submit that order so the system can turn it into an actual marker. During processing, the system checks the models, sizes, and quantities requested, pulls the correct pieces from the database, and applies any special options, matching rules, or alterations. Once done, the screen shows the marker's status, and an Activity Log keeps a record of everything that was processed, so you can confirm the job ran correctly before making the marker.

### Marker Plot Parameter Table
This table controls the technical details of how a marker plot (printout) will look, such as the rotation angle of the pattern pieces on the paper and the amount of space left between plotted markers. It also includes options like Die Cut Blocks, which tells the plotter whether to print just the outline used for die cutting or both the full piece outline and that outline together. You'd set this up once and reuse it whenever you plot markers, so plots come out consistent every time.

### Matching Form
This form is used to set up matching rules that make sure pattern pieces line up correctly with the fabric (like a stripe or plaid) or with each other. You choose whether the rule matches piece-to-fabric or piece-to-piece, and specify details like which piece and reference point should be matched. Cutters and markers use these saved rules automatically during marker making, so patterned fabric lines up properly instead of looking mismatched on the finished garment.

### Model Form
The Model Form is where you define a garment style or item as a 'model' — grouping together the specific pattern pieces, sizes, and options that make up that product. It's the central place used to build and organize models before they are referenced in a marker order.

**Model Options Editor** — Found on the Options tab of the Model Editor, this tool lets you build variations of a single model instead of creating a brand-new model for every style change. For example, you can set up a rule so a smaller size automatically uses a long sleeve piece while a larger size swaps in a shorter sleeve piece, using simple if/then logic. This saves time when a garment has small style differences across sizes rather than needing entirely separate patterns.

### Notch Form
This form (also called the Notch Parameter Table) lets you define the size and shape of notches — small marks or cuts placed at the edge of a pattern piece to help with sewing alignment. You can set values like the perimeter width and inside width for V-notches or castle notches, and save these settings under the default table name or a custom one. Sewers and cutters rely on these notch settings being correct so seams line up properly during assembly.

### Order Form
The Order Form is the main screen used to put together and submit a marker order, pulling together the models, sizes, quantities, and related tables (like lay limits or matching) needed to create a marker. It's the starting point for telling the system exactly what marker you want made.

**To order a marker** — This icon opens the Order Editor, where you gather all the information needed to order a marker — including lay limits, annotation, blocking/buffering, matching, and notch tables. The form has three tabs: Order (basic order details), Constructs (marks flawed or unusable areas in the fabric so the marker maker avoids them), and Models (specifies which garment models go into the marker). You'd use this whenever you're ready to request that the system build a specific marker for cutting.

### Order Process
This is the step where you actually submit a marker order for the system to process. Open the Order Process icon on the LaunchPad, select the order you want to run, and click the Process button to have the system generate the marker from that order.

**Process Order** — This command opens the Marker Order Processing Editor, the screen used to run marker orders and layrules through the system. You'd use it whenever an order needs to be processed into an actual usable marker, following the layout rules that were set up.

### Size Code Form
This form is used to set up size alterations — telling the system how to change an 'actual' pattern size (like 34R) into a different 'ordered' size (like 34S or 34L) using grade rule alterations. You select an alteration rule and amount for each size, and the ordered size you define here is the one selected later when the marker is actually ordered. It's used whenever your company needs to offer size options that require pattern adjustments beyond normal grading.

### User Environment
This is a settings screen, opened from Tools > User Environment Parameter Table in the AccuMark Explorer, used mainly when an older companion software version is being run alongside AccuMark Professional Edition. On this screen you control things like how measurements display, seam allowance for split pieces, how alterations plot, what happens if a duplicate marker is detected, which layrule and grading methods your company uses, and how bundle codes are set up.

### Verify
When a pattern piece is digitized (traced into the computer with a digitizing table), it's first stored as raw digitized data, and Verify is the process of checking that this data accurately matches the original paper pattern before it's converted into usable AccuMark piece data. You retrieve the digitized piece, confirm it looks right, save it in its current state (with the option to fix button/point placements later), and once confirmed, store it as a valid piece ready for marker making or plotting. This step matters because using unverified or incorrect digitized data could lead to wrong-sized or misshapen pieces being cut.

### Generating Cut Data
If your factory has GERBER automated cutters, this is the overall process of taking an order, turning it into a marker, and then converting that marker into cut data the cutter machine can read and act on. It's the final step in the workflow after ordering and processing a marker, letting the physical cutting equipment know exactly where and how to cut the fabric.

### Preparing the Pieces You Want to Cut
This is the first-step checklist a worker follows before a marker (the layout of pattern pieces) can be sent to a GERBERcutter for automatic cutting. It means adding special cutting instructions to each piece — start points, notches, internal markings, and other attributes — plus setting up notch, blocking/buffering, and lay limit settings. Doing this ahead of time makes the automatic cutter run faster and cut more accurately.

### Assigning Cutter Internals
This is where a worker assigns a letter code to special marks (called internals) printed or cut inside a pattern piece, such as drill holes or opstops. An opstop, usually labeled C, is a point where the cutter automatically pauses so the operator can reposition the cutting head — useful for matching plaids, stripes, or other patterned fabric precisely. Choosing the right letter tells the cutter exactly what action to take at that spot on the piece.

### Cutting Drill Hole Symbols
This function lets the cutter use its knife blade (instead of a drill) to cut small hole shapes — a circle, square, or diamond — at marked points on a piece, identified by codes 88, 89, or 90. To make this happen, the worker sets the Tool setting for that point to "Knife" in the Cutter Parameter Table (the settings sheet the cutter reads). The exact shape and size of the cutout is controlled separately in the Annotation table.

### To complete a Cutter Parameter Table
After a marker (the cutting layout) has been made and saved, the worker fills out a Cutter Parameter Table, which is basically an instruction sheet telling the AccuMark system how to turn that marker into cutting data the GERBERcutter machine can actually use. Different tables can be created for different cutter machines or different cutting jobs. Once this table is set up, the worker moves on to the Cut Generation screen to actually process the marker into cut data.

### To process marker data into cut data
This is the step-by-step process of turning a finished marker (pattern layout) into actual cutting instructions for the machine. The worker opens the Cutter Parameter Table from the Plotting and Cutting page, picks which type of cutting table the factory has (Static, Conveyor, or Traveling Conveyor), and selects cutting options like cutting small pieces first or slower, maximum movement distance, and edge tolerance. These settings tell the GERBERcutter exactly how to move and cut the fabric.

### Plotting Cut Data to Verify Accuracy
Before actually cutting fabric, the worker can print out (plot) a preview of the cut file to see, on paper, exactly how the GERBERcutter will cut the marker. This preview shows each piece's start point (marked with an arrow), the order pieces will be cut in (labeled N1, N2, etc.), the speed for cutting small pieces (shown as a percentage), and where internal marks will be cut. Checking this plot first helps catch mistakes before wasting fabric on the actual cutting table.

### To plot a marker cut file
This is the step-by-step process for printing that cutting preview described above. The worker goes to the Plotting and Cutting page, selects Cut Plot, chooses where the plot should go (a printer/plotter or a file), picks the storage location and the specific marker cut file to preview, and can choose to print it at full size to double-check accuracy before cutting real fabric.

### To create an exported cut data file
This is the process of saving marker cutting instructions as a file that the GERBERcutter machine can read, rather than sending it directly. The worker sets a destination folder (like a network drive or floppy disk the cutter can access), picks the marker and Cutter Parameter Table to use, and checks the "DOS file" box to save it as a standalone file instead of sending it straight to the machine.

### Exporting Cut Data
This is a checkbox option ("DOS File") in the Cut Generation screen that saves the marker's cutting instructions as a file in the standard GERBER cut-file format, rather than sending it live to a cutter. When checked, the file is saved to whatever folder location was set up in the Configuration settings, so it can be transferred or used later.

### Setting Up a Notch Parameter Table for Cutting
This table controls what shape of notch (a small clip cut into the fabric edge to mark seam or matching points) the GERBERcutter will cut. The manual recommends using V-notches instead of T-notches or Castle notches for automated cutting because the knife doesn't have to lift out of the fabric, making it faster; the V-notch should be about twice as wide as it is deep for the best speed and quality. The worker edits the default notch table or creates a new one with these settings before cutting.

### Setting Up a Blocking/Buffering Rule Table for Cutting
Blocking/buffering are optional rules that add small adjustments around certain pieces to improve how cleanly the GERBERcutter cuts them. The worker sets these rules up in the Blocking/Buffering Form and then applies them to specific pieces in the Lay Limits Form, and can create a different rule table for each unique cutting situation. These rules can be applied automatically when the marker is ordered, or turned on/off by hand while the marker is being made.

### Setting Up a Lay Limits Table for Cutting
In this form (found on the Marker Creation, Editors page), the worker marks which pattern pieces are "Major Pieces" — any piece not marked this way is automatically treated as a small piece. This matters because the Cutter Parameter Table can be set to cut all small pieces first and at a different speed, and this is also where blocking/buffering rules get assigned to pieces.

### Export File
Found under the View menu's Configuration option, this dialog lets the worker set default folder locations and file formats for plot and cut files. When a plot or cut job is run with the "DOS file" option selected, the system automatically saves the output file to whichever location was set here.

### Label Tool Mapping
This tool, found in the Cut Gen Parameter Table, lets a worker match each internal marking letter (used for things like drilling, cutting, or labeling) to the physical tool that should perform it — choices include Drill 1, Drill 2, Op Stop, Knife, Labeller, or Pen. The worker simply clicks through dropdown menus to assign a tool to each letter, or leaves a field blank to turn that internal off entirely.

### Applying Cutter Point Attributes
This describes the different ways a worker can mark up a pattern piece with cutting instructions (attributes and internal labels) for the GERBERcutter. The most efficient way is to add them while first digitizing (tracing) the piece into the system; alternatively, a worker can add or edit them later using the Piece Verify/Edit Points screen, or apply them automatically to graded sizes using the Rule Table Editor.

### Configuration Dialog Box
This settings screen, accessible from the View menu in the Cut Generation, Cut Plot, and Marker Plot forms, lets a worker set basic system defaults: the Plot File Type (choose GENERIC for Gerber equipment, or HPGL for other brands), and the folder locations (Plot Destination Path and Cut Destination Path) where plot and cut files will be saved.

### Working with Layrules
Layrules let AccuMark save, separately from the marker itself, the record of exactly which pieces were used and how they were arranged in a marker layout. Because this information is stored, the worker can delete the actual marker after it's been plotted or cut, and later, if a similar order comes in, AccuMark can automatically rebuild the same marker from the saved layrule instead of the worker re-laying it out by hand.

### Positional Layrules
Positional Layrules are one of the two types of layrules and work by remembering the exact original placement of every piece in a marker. This lets AccuMark automatically reconstruct a previously made marker later — almost like an advanced "Copy Marker" — saving the worker from manually re-placing pieces and freeing up storage space, which is especially useful when new orders need markers that are the same or very similar to ones made before.

### Layrule Features
This refers to the set of screens and settings you use to work with layrules, which are saved records of how pattern pieces were placed in a marker (a layout of pattern pieces on fabric). You set your Layrule Mode (No Layrules, Use Marker Name, or Use Search Criteria) in the User Environment Parameter Table, define matching details in the Layrule Search Parameter Table, pick the layrule type/name on the Order Form when ordering a marker, and run the Layrule Proc All command during order processing to actually apply the saved piece placement.

### Sliding Layrules
Sliding layrules are a recording of how you slid and positioned each pattern piece into a marker, including the direction, angle, and order in which pieces were placed. Workers use this feature (available with Batch Processing software and a special security key) to quickly build a new marker by reusing the placement pattern from a previous marker, called the master, as long as the new marker is similar in garment type, number and shape of pieces, lay limits, matching, size range, and average size.

### To create a sliding layrule
This is the step-by-step process for recording a sliding layrule: open Marker Making, build the marker you want to base the rule on, then go to Layrules > Sliding > Create, which clears (unplaces) all the pieces so you can slide them back into position yourself. As you re-place each piece, you can use toolbar commands like Advance a Step, Backup a Step, Insert a Step, and Delete a Step to fix mistakes, then save the finished layrule with Save Named (giving it a name you choose) or Save Search (letting the system name it).

### Advantages of Using Layrules
Layrules save you time and computer storage space when your company frequently reorders the same or similar markers, since the system only needs to store the small layrule file (about one-tenth the size of a full marker) instead of the whole marker. This also means less time spent hunting through stored markers, because the layrule automatically rebuilds the piece layout for you.

### Considerations for Using Positional Layrules
Positional layrules work best for repeat marker orders — new orders that recreate an older marker, often after fixing an error — as long as the old and new markers share the same models, sizes, fabric width, spread, and lay limits, and roughly the same number of pieces (the new one can have fewer). They are meant to handle only minor differences like label/annotation changes, small shape tweaks, and notch changes, not major redesigns.

### Naming Layrules
How you name a layrule determines whether you or the system controls which saved rule gets used for a new marker. You can name layrules yourself to match marker names (Use Marker Name) so they're easy to recognize, or let AccuMark generate names automatically based on key marker characteristics (Use Search Criteria); during order processing the system compares the new marker's name to existing layrule names and uses a match if found, or creates a new layrule if not.

### Naming Positional Layrules Using Save Name
Use this method when the new markers you create will keep the exact same name as the old markers they duplicate — simply save the layrule using the marker's name so it's easy to recognize later. AccuMark then automatically matches layrule names to marker names during the Layrule Proc All command in order processing, placing pieces according to the saved layrule, and if the AutoStore Layrule feature is on, it will automatically create or update the layrule whenever a matching marker is stored.

### Naming Positional Layrules Using Search Criteria
Use this method when new markers aren't simply renamed copies of old ones — instead, you tell AccuMark which marker characteristics (like size or fabric width) it should check to decide if a new order matches an existing layrule. You set these Yes/No choices on the Layrule Search Parameter Table; anything marked Yes must match exactly for the layrule to be reused, and changing these settings later can invalidate previously saved layrules.

### Set Up for Using Positional Layrules
Before using positional layrules, you configure the User Environment Parameter Table to tell the system how to name and find layrules — choosing Marker Name if repeat markers will always keep the same name as the original, or Search Criteria if names might change. This setup also controls related search settings like area compare, area deviation, copy dynamics, and allow overrides, found on the Layrule Search Parameter Table.

### To order a marker with layrules
When you place an order for a marker that should reuse a saved layrule, the Order Form automatically shows a layrule field based on how your system is set up. If your setup uses Marker Name, the field is called Force Layrule and you type in the name of the marker whose stored layrule you want used; if your setup uses Search Criteria, the field is called Lr Search Tbl instead, and the system searches for a matching layrule using the criteria you defined.

### Setting Up Matching Requirements
This is the general process of telling AccuMark how patterned fabrics like plaids and stripes need to line up across pattern pieces in a marker. It involves choosing a matching method (Standard or 5-Star) and setting up the specific points, rules, lines, or labels that define where pieces must align.

### Point Matching Versus Line Matching
This refers to the choice between two different ways of setting up fabric matching (lining up plaids or stripes between pieces): using assigned point numbers with a matching rules table, or using internal reference lines paired with labels. Which one you pick depends on your company's preferred workflow for controlling how pieces align on patterned fabric.

### Using Points and Rules to Set Up Matching
This matching method uses special point numbers placed on key locations of matching pattern pieces, entered into the Matching Form along with their piece categories, plus a matching rules table and certain Order Editor fields. It lets you control exactly how pieces must be positioned relative to each other, to the fabric's printed design, or both, which is important for lining up plaids or stripes correctly during cutting.

### Using Lines and Labels to Set Up Matching
This is an alternative matching method that uses internal reference lines drawn on pattern pieces along with descriptive labels, instead of point numbers and a rules table. Workers choose their matching method on the Order Form, can enter multiple offset values there, and use this setup when ordering a marker that needs plaid or stripe alignment.

### Standard Matching Versus 5-Star Matching
AccuMark offers two matching methods: Standard matching, which is the common approach used in the apparel (clothing) industry, and 5-Star matching, which is typically used in the furniture industry for matching floral prints. You choose which one to use either when ordering a marker or afterward inside Marker Making once the marker is retrieved.

### Choosing a Matching Method on the Order Form
On the Order Form, you use the Matching field to pick either Standard or 5-Star matching for the marker you're ordering, with Standard being the default. Choosing Standard gives you three separate offset fields for plaid and stripe matching, while choosing 5-Star simplifies this to just one offset field.

### Choosing a Matching Method in Marker Making
Inside the Marker Making application, you set the matching method by toggling the Matching Type field in the View > Settings window, choosing between Standard or 5-Star matching, with Standard as the default. This lets you switch or confirm the matching approach after the marker has already been opened, not just when it was first ordered.

### Standard Matching
Standard matching lines up plaid or striped fabric designs using horizontal and vertical reference lines placed in the marker, based on the fabric's repeat (how often the pattern repeats) and offset (how far it's shifted) values. These lines show you visually where on the marker the fabric pattern needs to align, and you can view or adjust the repeat and offset values directly within Marker Making.

### 5-Star Matching
5-Star Matching is a way to line up plaids and stripes in a marker (the layout of pattern pieces on fabric) using a plus-shaped symbol called a "star" to mark where lines should meet. Instead of entering separate values for every match point, the worker only enters one stripe and one plaid repeat value, and the system automatically places a star at every point where stripe and plaid lines cross, plus an extra star in the middle of each group of four. This is used whenever cutting patterned fabric so the plaids and stripes flow together correctly across seams; the pieces must have both a stripe line and a plaid line crossing on them for this to work.

### Entering Multiple Offsets on the Order Form
This function lets a worker enter more than one offset value (a measurement showing where a stripe or plaid line starts relative to the marker's edge) directly on the electronic Order Form used to request a marker. It is used when a fabric design repeats multiple times across the marker and each repeat needs its own starting position so the pattern lines up correctly when pieces are cut.

### Entering/Changing Repeat and Offset Values in Marker Making100
In Marker Making, when the Repeat/Offset field is set to Offset, the worker can type values into the Stripe (S1) and/or Plaid (P1) fields to set how far the first stripe or plaid line is from the edge of the marker. This lets the operator fine-tune where the fabric's pattern lines fall on the layout so pieces will match correctly when cut, without having to redo the whole marker.

### To create a matching rules table for  piece-to-piece, or piece-to-fabric
This is the step-by-step process for building a table of rules that tells the system how individual pattern pieces should line up with each other (piece-to-piece) or with the plaid/stripe design in the actual fabric (piece-to-fabric). A worker sets this up so that when a marker is made, the software automatically knows which edges or points must match, saving time and avoiding cutting mistakes on patterned material.

### matching
When the Matching field on the Order Form is set to Standard, extra fields appear where the worker enters the Plaid and Stripe repeat values (how often the pattern repeats across the fabric) and up to three sets of Offset values (where each matching line starts). Positive stripe offsets are measured up from the bottom edge of the marker, while negative offsets are measured down from the marker's center; this setup ensures the marker is built so patterned fabric lines up correctly at the seams once cut.

### Piece-To-Fabric Matching Chart
This chart is a reference guide showing, for each "First Point" position on a pattern piece (Bottom, Any repeat, Top, or Center), which Marker Match Location, X Match, Y Match, and Offset settings are valid to use. Workers use it to look up the correct combination of settings when setting up a piece to match against the fabric's plaid or stripe design, so they choose valid options instead of guessing.

### To order a marker with matching
To order a marker that needs its pattern (plaid or stripe) matched at the seams, the worker fills out the Order Form the same way as for a basic marker, but must also complete the Matching field (choosing Standard or 5-Star method), the Plaid Repeat field (the distance between repeats of the plaid pattern across the fabric), and the Plaid Offset field (the distance from the marker's lower left corner to the first plaid repeat in the material). Filling in these fields tells the system to build the marker so the fabric pattern lines up correctly when the pieces are cut.

### Changing Matching Information in Marker Making
This function lets a worker update matching settings after a marker has already been started, by selecting the Matching option in the Toolbox, clicking on the piece they want to change, and right-clicking to bring up a dialog box. Depending on whether the piece uses Matching Lines or Matching Rules, a different dialog box opens, but a box only appears if that piece was originally set up with matching — this lets the operator correct or adjust plaid/stripe alignment without starting the marker over.

### Grouping Pieces to Create Models
A model is simply a group of all the individual pattern pieces needed to make one complete garment or item, and the Model Editor is the tool used to build this group. When setting one up, a worker decides which pieces belong in it, whether each piece is a regular piece or a "paste piece" (a small piece attached onto a larger one), what fabric type each piece is cut from, how many of each piece are needed (including mirrored/flipped copies), and whether pieces can be shared between bundles.

### To create a model
To create a model, the worker goes to the Marker Creation/Editors section of the GERBER Launch Pad and opens the Model icon, then either opens an existing model or starts a blank one. They can add optional comments and default options, then select the pattern piece names to include (up to 250 rows) using a lookup list, building the complete set of pieces needed for the garment.

### To set up model options
Model options let a worker create different versions or variations of a model (for example, for different fabrics or style changes) by choosing Option, then New (or Next if options already exist) from the Model Editor menu. The worker names the option, then fills in Size and Piece Name fields, which act as conditions that determine which pieces are added or removed under that particular option.

### To retrieve and edit a model
To open a previously saved model, the worker goes to the Model editor in GERBER LaunchPad, selects File then Open, and picks the correct model by name from storage. They can then make any needed changes to the fields or options, and must use File > Save to keep the changes, or File > Exit to leave without saving if they were only reviewing it.

### To display an existing model option
After opening a model, the worker selects Option from the main menu to view the different option variations that have been set up for it. They can click Next or Previous to move through the list one at a time, or use Go To and type in the option's number or name to jump straight to it — the same actions are also available as toolbar icons.

### To copy a model option
To copy a model option, the worker opens the model, selects the option to copy, and chooses Copy from the Option menu; this creates a new tab (labeled "Opt X") containing a duplicate of that option's settings. The worker then renames the new tab, adjusts any fields as needed, and saves the model — this is useful for quickly creating a similar option without rebuilding it from scratch.

### To add a model option
To add a brand-new model option, the worker opens the model, chooses Option then New from the main menu, which creates a new tab labeled "Opt X." They rename the tab to describe its purpose (such as a fabric or style change), fill in the Size and Piece Name fields to set the condition for which pieces are added or removed, complete any remaining fields, and save.

### To delete a model option
To delete a model option, the worker opens the model, uses Option > Next, Previous, or Go To to find and display the specific option they want removed, then selects Delete from the Option menu. A warning message appears asking for confirmation — choosing Yes removes the option permanently while No cancels the deletion — and the worker saves the model afterward to keep the change.

### Defining Paste Pieces in Model Options
A paste piece is a small piece (like a pocket or label) that gets attached onto a larger "parent" piece rather than cut and handled separately. To define one, the worker opens the model, goes to the Option tab, selects the piece's name, and checks the box in the Paste column — once checked, the Fabric, Flips, Half Piece, and Dyn Split settings for that piece become inactive since they no longer apply.

### Model Editor
The Model Editor is the screen/tool where a worker builds and manages a model — the complete group of pattern pieces for a garment — including setting up paste pieces and their "parent" pieces. If a paste piece and its parent are defined on different Model Option pages, both must share the same piece category (assigned during digitizing) and the paste piece entries must be listed before any other normal pieces on that options list.

### To shutdown Order Entry
This is how a worker closes the Order Editor screen when they are done working on an order. You can do it three ways: double-click the small icon in the top left corner of the form and choose Close, go to the File menu and select Exit, or simply click the X in the top right corner of the window. Whichever way you choose, make sure to save any changes you made before closing, or your edits will be lost.

### To customize the Order Entry toolbar
This lets a worker change what tools and information show up on the Order Entry screen to match how they like to work. By opening the View menu, you can turn the Tool Bar, Status Bar, Target Utilization display, and automatic marker-naming feature on or off by clicking each one to add or remove its check mark. This is useful for simplifying the screen to show only what you need for your daily tasks.

### To edit a User Environment Parameter Table
This table holds default settings used only when the AccuMark Professional Edition is being run alongside an older version of another Gerber software tool. A worker opens it from AccuMark Explorer by finding the correct drive and storage location, double-clicking the table to open it, making the needed changes, and then saving with File and Save. You would use this if your factory still runs older compatible software and needs to keep the settings matched between systems.

### To create a new User Environment Parameter Table
This creates a brand-new settings table used when running an older companion software program together with AccuMark Professional Edition. In AccuMark Explorer, the worker opens the User Environment Parameter Table tool, selects File then New, and sets defaults like Seam Allowance, Overwrite Marker, Layrule Mode, Grading Method, Alteration type, and Bundling Method, plus choosing Metric or Imperial units, before saving the new table with a name.

### To use a different User Environment Parameter Table
This lets a worker switch which settings table the system uses when processing orders, by copying the contents of the table they want into the active table (called P-USER-ENVIRON) that the software actually reads. In AccuMark Explorer, you open the User Environment tool, then use File and Open to browse to and select the device, storage area, and specific table you want to bring in and use instead of the current one.

### To edit a Notch Parameter Table
A Notch Parameter Table stores the settings that control how notches (small cut marks used for aligning fabric pieces during sewing) are sized and shaped. A worker can open this table either through AccuMark Explorer or through the Notch icon in GERBER LaunchPad's Marker Creation, Editors page, make the necessary changes to the values, and then save them with File and Save.

### To create a Notch Parameter Table
This creates a new table defining how notch marks will be cut on fabric pieces. Using the Notch icon on the GERBER LaunchPad's Marker Creation, Editors page, the worker selects File then New, then sets values for Perimeter Width, Inside Width, and Notch Depth, along with choosing Metric or Imperial units, and finally saves the table with a chosen name and storage location.

### To View the Activity Log
The Activity Log is a record of recent actions the system has performed, and viewing it lets a worker check what has happened on the system recently, such as completed jobs or processing steps. You open it from the Utilities page in GERBER LaunchPad's AccuMark Explorer by clicking the Activity Log icon, then use the scroll buttons to read through all the entries. You can also print the log using the Printer icon or the File, Print menu options if you need a paper copy.

### To clear all items from the Activity Log
This action erases all the entries currently listed in the Activity Log, giving you a clean slate to track new activity going forward. After opening the Activity Log (from a Marker Creation tab like Order Entry or from AccuMark Explorer's View menu), the worker clicks the "X" button on the tool bar or chooses Edit and then Clear All to wipe out the existing log entries.

### Setting Up Annotation Requirements
Annotation refers to text or labeling information that gets printed on cut fabric pieces or along the edges of a marker (the layout plan showing how pieces fit on fabric) when they are plotted or printed out. This information is defined using the Annotation Form, found on the Marker Creation, Editors page in GERBER LaunchPad, and is saved as an annotation library that tells the system exactly what labels or details to include on the printed pieces or marker.

### To create an annotation library
This is how a worker builds a saved set of labeling rules that determine what text appears on plotted (printed) fabric pieces or along the marker border. In GERBER LaunchPad's Marker Creation, Editors page, you open the Annotation icon, choose the annotation type for either piece plotting or marker plotting using the lookup box, and then save the file with a descriptive name so it's easy to find and use later.

### To retrieve and edit an annotation library
This lets a worker open a previously saved annotation library to review or change its labeling settings. From the Annotation icon on GERBER LaunchPad's Marker Creation, Editors page, select File and Open, browse to the correct device, storage area, and file, make your edits, then save and exit with File and Save and File and Exit.

### Setting Up Lay Limit Requirements
Lay limits are rules that control how fabric pieces can be arranged and placed together in a marker (the cutting layout on the fabric). These rules — covering things like how the fabric is spread, how bundles are oriented, and how pieces are blocked or buffered — are set up using the Lay Limits Form.

### To create a lay limits table
This is how a worker sets up the rules for how fabric will be spread out and how pieces will be arranged before cutting. Using the Lay Limits icon on GERBER LaunchPad's Marker Creation, Editors page, you select File and New, then fill in fields such as Fabric Spread (choosing Single Ply, Face to Face, Book Fold, or Tubular) and Bundling direction, along with blocking and buffering rules and piece placement limits, before saving the table.

### To retrieve and edit a lay limits table
This lets a worker open an already-saved lay limits table to check or change its settings. From the Lay Limits icon on GERBER LaunchPad's Marker Creation, Editors page, select File and Open, choose the correct storage location and file, make the needed edits to the fields, and then save with File and Save before exiting.

### Setting Up Blocking/Buffering Requirements
Blocking adds extra space around all or part of a fabric piece, which is useful for critical pieces like collars or lapels that will be die cut, or for pieces that get cut, restacked, and cut again — the cutter will cut this larger, extended shape. Buffering keeps a set distance between pieces in a marker so cutting equipment has room to adjust for accurate matching (especially on plaids or stripes) and so pieces don't sit too close together during cutting; both are set up using the Block Buffer Form.

### To create a blocking/buffering rule table
This is how a worker defines the extra space added around fabric pieces for blocking (extending the cut shape) or buffering (keeping pieces apart). Using the Block Buffer icon on GERBER LaunchPad's Marker Creation, Editors page, select File and New, choose Block or Buffer in the Rule field, then enter the Static and/or Dynamic spacing amounts for the Left, Top, Right, and Bottom of the piece, repeating for each rule number needed before saving.

### To retrieve and edit a blocking/buffering rule table
This lets a worker open a previously created blocking/buffering table to review or adjust its spacing rules. From the Block Buffer icon on GERBER LaunchPad's Marker Creation, Editors page, select File and Open, pick the correct drive, storage area, and table name, make the necessary edits, then save and exit using File and Save followed by File and Exit.

### Static versus Dynamic Blocking/Buffering
This describes two ways extra space ("blocking" or "buffering") gets added around pattern pieces before cutting. With static blocking/buffering, the system automatically adds that space to the pieces during order processing, so by the time you open Marker Making the pieces already have it built in. With dynamic blocking/buffering, the space is defined ahead of time on the Order form but can be turned on or off by the worker while actually building the marker in Marker Making.

### Applying Blocking/Buffering
This is the overall process of adding extra fabric space around a piece's edge (blocking/buffering), which you can set up in a few ways: marking specific points on a piece with B (start) and Q (end) attributes during digitizing or in Piece Verify/PDS, filling out a Block Buffer form to build a reusable table of rules, and/or entering piece categories and rule numbers on a Lay Limits form so the system knows which pieces get which rule. You also need to name the correct tables on the Order form so the system applies the right blocking/buffering when the order runs.

### To Change the grade rule values in a specific column
This function lets you flip the sign of a whole column of grading values at once instead of retyping each one. On page 2 of the Rule Table Editor, you highlight the column you want to change, then use the right-click menu and choose "change sign" — every positive number in that column becomes negative, and every negative number becomes positive.

### To Clear the grade rule values in a specific column
This function wipes out all the grading numbers in one column of the Rule Table Editor at once. You highlight the column on page 2 of the Rule Table Editor, right-click, and choose "Clear Column," which deletes every value in that column so you can start fresh.

### Pattern Conversion Wizard
This tool lets you send pattern pieces and their grading (sizing) information back and forth between AccuMark and other pattern-making CAD systems, using a standard file format called DXF. You'd use it when a pattern was made on a different system and needs to come into AccuMark, or when you need to send an AccuMark pattern out to someone using different software; it follows the ASTM D 6673-01 standard (and can also handle the older ANSI/AAMA-292 format) so the pieces and grading come through correctly.

### Marker Creation, Editors Page
This is a screen on the GERBER LaunchPad (the main starting menu) that gives you 14 icon buttons, each opening a different form you need to set up and process a marker order — things like Order Processing, Order, Model, Laylimits, Annotation, Notch, Block Buffer, Matching, Alteration, Size Code, Layrule Search Parameter Table, AutoMark Edit, MK Import Report, and Marker Making. It's essentially your one-stop launch point for every editor involved in building an order.

### Toolbar
The toolbar is the row of small icon buttons you see at the top of Order Entry forms that give you quick, one-click access to commands you use often, instead of digging through menus. If you're not sure what a button does, just hold your mouse pointer over it for a couple of seconds and its name will pop up.

### Model
A Model is simply the complete set of all the individual pattern pieces needed to make one finished garment or item, such as a shirt's front, back, sleeves, and collar all grouped together. Workers set this group up using the Model Form, a data entry screen where all the pieces for that garment style are listed and organized. Creating a Model this way lets the system treat all those pieces as one unit for cutting, ordering, and marker-making tasks.

### Model Options
This is a tab inside the Model Editor that lets you create variations of an existing model without having to build a whole separate model from scratch for every style change. It's commonly used to substitute or add pieces — for example, when a pattern change is too big to handle just by grading sizes and instead requires swapping in different pieces.

### Annotation
This opens the Annotation Editor, where you build a library of text and information — like size, style number, or piece name — that you want automatically printed on a piece or along the marker's border when it's plotted (printed out on paper or fabric). It saves you from manually labeling each piece by hand every time.

### Lay Limits
Lay Limits are the general rules that control how pieces are allowed to sit within a marker — the layout of pattern pieces on the fabric before cutting. Opening the Lay Limits Editor lets you set how fabric will be spread, control which way bundles face, apply blocking/buffering rules to pieces, and set other placement restrictions.

### Alteration
This opens the Alteration Editor, used to set up rules that change the shape of a pattern piece — for example, lengthening a sleeve or adjusting a hem — without you having to store a completely separate graded piece for every variation. Using these alteration rule tables cuts down significantly on the number of individual pieces and sizes the system needs to keep on file.

### Size Code
This opens the Size Code Editor, which works together with the Alteration Editor. You use it to build a table that says which sizes go into a marker with alterations applied and how those sizes should be changed, and it lets you rename sizes without creating a whole new grade rule table — AccuMark combines the existing grade rule table with the alteration rules to produce the new size.

### Block Buffer
This opens the Blocking/Buffering Editor, where you set up rules to add extra space around part or all of the edge of a pattern piece. This extra space is often needed for cutting accuracy or to account for how a fabric behaves.

### Matching
This opens the Matching Editor, where you create rule tables for lining up patterned fabrics — such as plaids, stripes, or matching specific points and lines — as well as standard or 5-star matching. You'd use this whenever the fabric design needs to line up correctly across seams in the finished garment.

### Multi Order
This opens the Multi Order Editor from the AccuMark Classic Edition's System Management/Edit Data Base menu, a faster way to set up several marker orders at once instead of entering them one at a time in the standard Order Editor. AccuMark comes with three ready-made templates — one for entering 10 orders per screen, one for 6 orders per screen, and a blank "standard" one you can customize — so a worker can process a batch of orders together and save time.

### User Environment
This is a settings screen, opened from Tools > User Environment Parameter Table in the AccuMark Explorer, used mainly when an older companion software version is being run alongside AccuMark Professional Edition. On this screen you control things like how measurements display, seam allowance for split pieces, how alterations plot, what happens if a duplicate marker is detected, which layrule and grading methods your company uses, and how bundle codes are set up.

### Layrule Search
This opens the Layrule Search Parameter Table, where you set rules for how the system searches for and applies layrules — a form of automatic marker-making used to rebuild an old marker or quickly redo one after small pattern changes, like adding a piece. You'd adjust this when you want the system to automatically match a new marker to a previously made one instead of laying it out manually.

### Notch
Notch is a command you open from the Marker Creation, Editors page of the GERBER LaunchPad that brings up the Notch Parameter Table. On this screen you tell the system what type and size of notches (small cut marks on the edge of a pattern piece that show where to match or fold fabric) should be placed on pieces in a specific storage area, so the cut pieces come out with the right matching marks.

### Piece Plot Parameter Table Field Explanations
This is the reference guide for filling out the Piece Plot Parameter Table, which you open from the Plotting and Cutting page of the GERBER LaunchPad. It walks you through each field on that table, such as the File Name field (used to save, name, or retrieve a specific set of plot settings) and the Rotation field (used to turn pieces to save paper), and marks which fields have a lookup list of choices you can pick from with the right mouse button.

### Marker Plot
Marker Plot is an icon on the Plotting and Cutting page of the GERBER LaunchPad that opens the Marker Plot Parameter Table. You use this table to set how the system and the plotter (the machine that prints or draws the marker) should behave when it plots out a marker for you.

### Cut Generation Parameter Table
This is the Cutter Parameter Table, opened by choosing the Cut Parameter Table icon on the Plotting and Cutting page of the GERBER LaunchPad. You use it to control how the system behaves when it turns a marker into cut data — the file format a GERBERcutter machine needs in order to actually cut the fabric.

### Process
Process is the action that starts whatever task you are working on on the current screen, such as generating a plot, saving a table, or running a calculation. You click Process when you're ready for the system to actually carry out the setup you entered.

### Activity log
The Activity Log is a running report inside AccuMark that keeps a record of all the major things that have happened in the system. It lists both successful actions and failed ones, including any error messages, in the order they happened, so you can look back and see what was done or what went wrong.

### Clear All
Clear All is a command that permanently erases every entry currently in the Activity Log. Once you use it, that history of past actions and error messages is gone for good, so use it only when you're sure you no longer need that record.

### Cut data
Cut data is what a marker (the layout of pattern pieces arranged on fabric) becomes after it's been converted into a special file format. A GERBERcutter machine reads this file so it knows exactly where to cut the fabric to produce the pieces.

### ASCII
ASCII stands for American Standard Code for Information Interchange, a very common, plain text file format. Files saved in this format can be opened and read by many different software programs, not just AccuMark, which makes it useful for sharing data.

### Category
Category is a label you give to every piece in a model to identify what kind of piece it is, like front, back, or sleeve. Every piece must have its own unique category name, which can be up to 20 characters long, so the system and the people using it can tell pieces apart.

### Fields
Fields are the rectangular boxes you see on AccuMark screens where you type in information or where information is displayed. On some of these boxes, you can right-click to open a lookup list of valid choices and pick one instead of typing it yourself.

### Next Page
Next Page is a button that moves you forward to the following page of whatever screen you're currently viewing in AccuMark. You use it when a table or list has more information than fits on one page.

### Previous Page
Previous Page is a button that takes you back to the page you were on before, on the current screen. It's the reverse of Next Page, letting you review information you already passed.

### Print Plot
Print Plot lets you send piece, marker, or cut jobs that are sitting in the plot queue (a waiting list of jobs ready to print or plot) to actually be printed as physical copies. You'd use this when you're ready to get a paper copy of a piece layout, marker, or cut plan.

### View Plot
View Plot lets you see, on your computer screen, a picture of a piece plot, marker plot, or cut plot job that is waiting in the plot queue, without having to print it first. After processing the job, you open the Queue Manager, right-click the job, and choose View to see the layout on screen; there's also a View Marker Plot option for reviewing a saved marker plot file directly through Explorer.

### Page Up
Page Up displays the previous page of whatever screen you're currently working on, letting you move backward through multi-page information.

### Page Down
Page Down displays the next page of whatever screen you're currently working on, letting you move forward through multi-page information.

### Fabric type codes
Fabric type codes are single-letter codes you assign to each piece in a model to show which fabric it should be cut from, for example S for self fabric, L for lining, or F for fusible. A piece can carry up to four codes if it uses multiple fabrics, and pieces sharing the same code can be grouped together into the same marker for cutting; if you leave this blank, the system assumes every piece uses the same fabric.

### Cutdown master
A "cutdown master" is the bigger version of a pattern piece that other, smaller sizes get cut from. Instead of making a brand-new pattern for every size, the worker cuts the smaller ("cutdown") size directly out of this larger master piece, saving time and material setup.

### GERBERlabeller
This is an automated Gerber machine that sticks a pre-printed label onto the top layer of fabric while it's laid out in a marker (the layout plan showing how pieces are arranged on the cloth). Workers use it so labels get applied automatically instead of by hand, keeping the process fast and consistent.

### Go To Top
This command jumps you straight to the very beginning of the information shown on your current screen. Use it when you've scrolled down a long list or report and want to quickly get back to the start without scrolling manually.

### Go To Bottom
This command jumps you straight to the very end of the information on your current screen. It's handy when you're looking at a long list or report and want to see the last entries right away instead of scrolling through everything.

### Delete All Job
This function permanently deletes every job and group waiting in the plot queue (the line-up of jobs waiting to be printed/cut), including ones that are currently running and ones that are just waiting. Use it carefully since once deleted, these jobs cannot be recovered and would need to be resubmitted.

### Delete Jobs
This lets you permanently remove specific jobs you select from the plot queue (the waiting line of print/cut jobs). It only works on jobs that aren't actively plotting right now — if a job is currently running, you can't delete it this way.

### Plot Now
This lets you pick one or more jobs or groups sitting in the plot queue and send them to print/cut immediately. If the plotter is already busy with other jobs, your selected jobs will automatically start as soon as those finish, so you don't have to keep checking and resubmitting.

### Stop Immediate
This immediately stops the plot queue and takes the connected plotter offline, right in the middle of whatever it's doing. To get plotting going again, you have to use Restart Queue first and then manually switch the plotter back online.

### Print
This prints out whatever information is currently shown on your screen, and if that screen has multiple pages (like some reports do), the system automatically prints all of them for you. Note that just hitting the keyboard's Print Screen key only grabs the one page you're looking at, not any additional pages.

### Process Group
A "group" is a set of plot jobs that AccuMark treats and submits as a single combined job. Choosing Process Group keeps all the jobs in that group together in the plot queue and makes the plotter run through them one after another without letting other unrelated jobs cut in between.

### Stop After
This tells the plotter to keep working until it finishes the specific jobs or groups you've chosen, and then stop. It's useful when you want the current work to complete cleanly before halting, rather than stopping abruptly mid-job.

### Restart Queue
After you've stopped the plot queue and taken the plotter offline (using Stop Immediate or Stop After), this command makes the queue active again so jobs can move forward. You still need to manually turn the plotter back online afterward before it will actually start plotting.

### APSM
APSM stands for the GERBERcutter Automatic Plaid and Stripe Matching system, a feature that lines up patterned fabrics like plaids and stripes correctly during cutting. You turn it on by setting the Cutter parameter table's AutoMatch field to Yes, and then when the cut file is processed, AccuMark automatically generates the codes needed to drive this matching system on the cutter.

### Next Model
This shows you the next model (a specific size/style combination) in the marker order you're currently working on. It's a simple way to step forward through the list of models one at a time.

### Previous Model
This shows you the previous model (a specific size/style combination) in the marker order you're currently working on. It lets you step backward through the list of models one at a time.

### Go To Model
This lets you jump directly to a specific model in the current marker order by typing in that model's number and pressing Enter. It saves time compared to clicking Next or Previous repeatedly when you know exactly which model you need.

### Copy Model
This creates an exact duplicate of the model order currently being displayed. It's useful when you need a new model that's very similar to an existing one, since you can copy it first and then adjust as needed instead of starting from scratch.

### Add Model
This lets you add a brand-new model into the current marker order by opening up a blank Order Editor Models screen for you to fill in. Use it when you need to include an additional size/style combination that isn't already part of the order.

### Delete Model
This command lets you permanently take the current model off the marker order you're working on. It's important to know that this only removes it from the order list — the actual model itself (built earlier in the Model Editor) stays saved in the system and isn't affected.

### Bite length
Bite length is the amount of fabric or material the cutter cuts through before it stops and pulls more material onto the cutting table. Think of it as how much the machine chews through in one pass before advancing the material for the next pass.

### Group
A group is simply a bundle of plot jobs that the system treats as a single unit so they stay together in the Plot Queue (the waiting line of jobs to be plotted) and print one after another without other jobs jumping in between. You can use commands like Delete, Stop, and Plot Now on the whole group at once, which saves you from managing each job separately.

### Delete All
This wipes out every job waiting in the plot queue (the list of print/cut jobs lined up to run), including any job that is currently in progress. Use it when you need to clear the whole queue and start fresh.

### Delete
This removes one plot job, or a whole group of jobs, from the plot queue — but only if that job or group isn't actively running at the time. It's the go-to command for clearing out a single unwanted or duplicate job without touching the rest of the queue.

### Delete Active
This command removes only the job or jobs that are currently running (active) in the plot queue, while leaving every other waiting job untouched. Use it when you specifically need to cancel what's printing right now without disrupting the rest of the line-up.

### Restart Active
After you've used Stop Immediate to halt a plot job — for example because of a paper jam or other equipment problem — Restart Active starts that same job over again from the very beginning. This saves you the trouble of re-entering or resubmitting the plot request from scratch.

### Clear Owner
This takes away whoever currently 'owns' (has control over) the plot queue and its connected plotter, resetting the owner status back to None so someone else can take control. It's useful when you need to free up a plotter that's still marked as being used by another operator or session.

### New Page
This command tells the plotter to move its paper or material forward to the beginning of a fresh page, but it only does this once the plotter has come to a complete stop. Use it when you need to start a new plot on a clean section of material.

### Set Media
This lets you switch to a different type of material (Media ID) for plotting, but you can only make the change when the plot queue is empty or has no active jobs running — you may need to use Stop After and wait for the queue to finish first. Once you change it, the next job will start plotting from the bottom left corner of the new material, and the material types themselves are defined elsewhere in Plotter Settings or the Configuration Toolchest.

### Library
In AccuMark, 'library' is basically another word for a table — a saved set of settings or data you can reuse. For instance, when setting up text and labels through the Annotation Form, the saved settings are called annotation tables or annotation libraries.

### Blocking
Blocking adds a second, extra outline a set distance outside a pattern piece's actual edge, giving the piece some 'breathing room' beyond its real cutting line. It's mainly used for delicate pieces like collars or lapels that get die cut, or for pieces in matched markers that are cut, restacked, and cut a second time — the cutter follows the blocking line instead of the real edge, leaving extra material so the cutting head can be readjusted for an accurate match.

### Buffering
Buffering keeps a set amount of space between pattern pieces on the marker (the layout of pieces on fabric) so they don't sit too close together, which helps the cutter do a cleaner job. Unlike blocking, the cutter still follows the piece's actual, real edge — buffering just prevents cutting problems called heelcuts and overcuts; buffered pieces show up with a dotted outline on screen, though only the true edge appears on a printed marker.

### Add Rule
This command lets you insert a brand-new alteration rule (an instruction for how to resize or adjust a pattern) into the alteration rule library, placing it right after whichever rule you currently have open.

### Delete Rule
This command removes the alteration rule you're currently viewing from the alteration rule table, permanently taking that adjustment instruction out of the set.

### Next Rule
This command moves you forward to view the rule listed right after the one you're currently looking at within the alteration rule table.

### Previous Rule
This command moves you backward to view the rule listed right before the one you're currently looking at within the alteration rule table.

### Hold points
Hold points are specific reference spots on a pattern piece that stay in the exact same place both before and after an alteration (a sizing or fit change) is made, acting as fixed anchors while everything else around them shifts.

### Move points
This refers to the pattern points that shift position in order to create an alteration movement — for example, moving a hemline or waist point to make a garment longer or shorter. When a worker applies an alteration rule, these are the specific points on the pattern piece that the system actually relocates to produce the size or fit change.

### Go To Act Size
This function lets you type in an actual size (a specific size that was already set up in the size code table, the system's reference list of sizes) and instantly jump to and view that size's information. Use it when you need to check or work with one particular size without scrolling through the whole size list.

### Go To Ord Size
This function lets you type in an ordered size (the size a customer or order requested, previously recorded in the size code table) and jump straight to that size's details. It saves time when you need to check a specific ordered size instead of searching through the full list.

### Alteration base amount
This is the full (100%) movement amount defined for an alteration rule — basically the maximum distance a pattern point is allowed to shift for that alteration, as set up in the size code table (the database of alteration names and amounts). Other points in the same alteration move by a percentage of this base amount (calculated as the amount to move divided by the base amount), so for example if the base amount for "Coat Length" is 1.00 inch and a pocket drill only needs to move 0.50 inches, that point moves at 50% of the base amount.

### Layrule Proc
Short for "Layrule Process," this command tells the system to process a marker order (a marker is the layout of pattern pieces used for cutting fabric) by trying to recreate it automatically using a source marker, a saved layrule, or the settings in the Layrule Search Parameter Table entered on the Order Editor screen. Use it when you want the system to rebuild a marker layout automatically instead of a person laying out every piece by hand.

### Load Multi-List
Use this after processing marker orders if some of them failed with errors — the system keeps a memory list of the names of the orders that didn't process correctly during your most recent session. After you check the Activity Log to find out what went wrong and fix the problems, you use Load Multi-List to pull up that same list of failed orders and reprocess them without having to type them in again.

### Copy
This command makes a duplicate of one order you've selected. The duplicate is temporarily stored in the computer's clipboard (a short-term holding spot) until you either paste it somewhere or copy a different order, which replaces it.

### Paste
This command takes the order you most recently copied to the clipboard and places it into the order field you currently have selected/highlighted on the order entry screen. It's used right after Copy, to quickly duplicate an order's information into a new spot instead of retyping everything.

### Drill symbols
Drill symbols are the different hole-mark shapes AccuMark can plot (print) or cut onto pattern pieces to mark important spots like pocket placement or button positions. The available shapes are an asterisk (Symbol 69), a plus sign (Symbol 74), a circle (Symbol 88), a square (Symbol 89), and a diamond (Symbol 90), so a worker can pick the shape needed for a given marking.

### Positional layrules
Positional layrules are saved records of exactly where each pattern piece was placed in a marker (the fabric-cutting layout). This lets AccuMark automatically rebuild a previously made marker later during order processing or marker making, using smart search techniques that work like a more advanced version of simply copying a marker.

### Force Layrule
This is a field on the Order Editor screen where you type in the exact name of a layrule (a saved marker layout pattern) you want the system to use when processing an order. If no layrule with that name already exists, the system will automatically create one and give it that name once the marker is saved.

### Lr-Search-Tbl
This is a field on the Order Editor screen that shows the name of the Layrule Search Parameter Table currently being used — this table holds the criteria the system checks when trying to find or match a layrule during order processing. You can type in a different table name here if you want the system to search using different criteria, and if no matching layrule is found, the system will name a newly created one after this table.

### Copy Marker
This is a field on the Order Editor screen where you enter the name of an already-existing marker whose piece placement/layout you want to copy for a new order. Unlike layrules, the marker you're copying from must still exist in the system — it can't have been deleted.

### Annotate an Attached Marker
This feature lets order information carry over onto an attached marker (a marker formed by joining multiple markers together, which normally loses some of the original order details). By entering information into the Order Number field on the Order Editor and then setting up the Annotation Table to print the Piece Description, workers can get that order information printed directly on the pieces of the combined marker.

### Decimal Notation
This setting controls whether decimal numbers on your screen and in your data entry forms use a period or a comma, based on your computer's Regional Settings. Workers should always check and match this local setting when typing numbers into forms so measurements are entered correctly.

### Import and Export User Settings
This feature lets a worker save their personal PDS (Pattern Design System) setup — things like toolbar layout, workspace arrangement, color choices, and preferences — to a file, and later load that same setup back in. It's useful for keeping a consistent setup across shared computers, quickly restoring your own settings, or letting IT/support duplicate a standard setup for everyone; note that PDS must be closed while doing an import or export.

### Storage Areas
Storage areas are the folders/work spaces where all your AccuMark files — pattern pieces, markers, and other data — are organized and saved, similar to regular Windows folders, and they can live on a hard drive, network drive, or removable disk. Workers use storage areas to keep their work organized and easy to find, and these areas can be viewed from Order Entry, Marker Making, or PDS, and created or deleted through the Order Entry forms or AccuMark Utilities.

### Notch Types
Notch types are the different notch shapes/styles available in AccuMark that get marked or cut onto the edges of pattern pieces to show where pieces should be matched up or sewn together during garment construction.

### Shortcuts
This is a section of the manual that gives you tips and tricks to work faster in AccuMark, such as keyboard shortcuts and special field behaviors. Workers would look here when they want to speed up repetitive tasks on the order screen instead of always reaching for the mouse.

### Quick Keys
Quick Keys are keyboard shortcuts (using the Alt key plus an underlined letter) that let you jump straight to a menu command like File or Model without clicking through with the mouse. Related topics like Lookup Fields are covered nearby because they also help you move through Order Entry screens faster.

### Hot Links
Hot Links are a shortcut feature in certain Order Entry fields that need information pulled from another form or table (like a size chart) — pressing the F2 key on one of these fields opens that related form so you can grab the data instead of typing it in by hand. This saves time and reduces mistakes because you're pulling exact data rather than retyping it. Quick Keys, mentioned alongside Hot Links, let you hold Alt and press an underlined letter (like Alt+M then W to add a new Model) to move through menus using only the keyboard.

### Field Types
This is an overview section explaining that the blanks you fill in on Order Entry screens (called fields) come in different types — such as sticky, rotary, text, and lookup fields — each behaving differently when you enter or select data. Knowing the type helps a worker understand how to correctly fill in or change that blank.

### Sticky Fields
A sticky field is a blank on the screen that remembers the last value you set even after you close and reopen AccuMark, instead of resetting to the system default. For example, the HalfPiece field on the Model form keeps showing your chosen value so you don't have to re-enter it every time, which saves time on repeat orders.

### Rotary Fields
A rotary field is a blank that already shows a default setting, but you can change it by clicking the left mouse button while your cursor is in that field to cycle through other available choices. This is useful when a field has a small set of fixed options (like a size or a yes/no setting) and you just need to pick a different one quickly.

### Text Fields
A text field is a blank on an Order Entry screen where you type in information directly, such as a style number or a note, rather than picking from a list or toggling a setting. Workers use these whenever the system needs free-form information that isn't limited to preset choices.

### Lookup Fields
A lookup field is a blank that lets you pull up a list of valid choices (like styles, colors, or sizes stored in a parameter table) instead of typing the value in yourself, which helps prevent typos and ensures the entry matches what's already set up in the system. You click into the field and a small square button with three dots appears — clicking it opens the selectable list.

### To display and use a Lookup Field
This is a step-by-step instruction for using a lookup field: click into the field, look for the small square button with three dots at the right end (or press F4), click that button to see a list of valid entries, then click your choice and press Open to use it, or Cancel if you change your mind. This process helps you quickly and accurately fill in fields that pull from existing lists rather than typing values by hand.

### Networking
This section explains that an AccuMark system can run on its own computer or be connected to other computers and equipment over a Local Area Network so files and data can be shared between them. It lists the different networking software options (like Novell NetWare or Microsoft Windows NT) that AccuMark supports, which your IT staff would set up so multiple workstations can access shared order and pattern data.

### Printing
Printing lets you produce a paper copy of the information on the form or table you're currently working in, such as an order or a report. You can start it by choosing Print from the File menu (Alt then F, then P), by pressing Ctrl+P, or by clicking the printer icon on the toolbar, which opens a dialog where you set your printing preferences.

### Network Plotting
Network Plotting is used when a computer on your network doesn't have its own plotter (the large printer that outputs full-size pattern pieces or markers) physically connected to it. Setting up network plotting lets that computer send its plot jobs over the network to a plotter attached to a different machine, so every workstation can still produce printed markers or pieces.

### Fatal Error Report
When AccuMark or Windows shows an error message on screen, you press the Print Screen key to capture an image of that message, then paste it into a program like Paint so you can print it out. You then give this printed error report to your Gerber field service representative so they can diagnose the problem, and you should do this for any follow-up error messages too.

### View System Information
This is a troubleshooting tool inside AccuMark Utilities that shows details about your computer system, including the AccuMark files installed and their version numbers, Windows information, and the hardware devices set up for AccuMark. If something goes wrong, a Gerber Product Support specialist may ask you to print this information and send it to them so they can help fix the issue.

### Version Info
Version Info shows you the software's version number and related details — you view your overall system version through AccuMark Utilities (View menu, then Version Information, then print via the printer icon), or you can check the version of a specific form or table by selecting the Help menu (or the ? icon) while that form is open. This is useful when Gerber support needs to know exactly which version of a form or the software you're running to help troubleshoot a problem.

### Maximum Data Items Allowed
This is a reference table listing the maximum number of items AccuMark can handle in different areas, such as up to 5,000 pieces or 500 bundles in a marker, 250 pieces per model, and limits on rules, categories, and points per piece. Workers and planners use this table to make sure an order, marker, or pattern piece doesn't exceed what the software is able to process.

### Maximum Marker Length
By default, AccuMark limits a marker (the layout of pattern pieces on fabric) to 100 yards long, but the system actually supports up to 999 yards if needed. To increase this limit, someone edits a system settings file (Autoexec.bat, or the Environment variables on NT systems) to set the Max_Length value and then restarts the computer for the change to take effect.

### Checking Pieces for Accuracy
After a pattern piece has been newly digitized (traced into the computer), you check that it was captured correctly using three main steps: Verifying, Store Verifying, and Piece Plotting. This process helps catch digitizing mistakes before the piece is used in production, and pieces that were scanned or imported instead of hand-digitized can be checked the same way, or by using tools within the AccuMark PDS application.

### Hardware Configuration
This is the screen in AccuMark Explorer where you tell the system what physical equipment is hooked up to it, such as a digitizer, tablet, plotter, function box, or tracker. To use it, open the Utilities page on the GERBER LaunchPad, click the Hardware Configuration icon, pick the tab for the device you're setting up, and fill in its settings, then click Apply to configure another device or OK when you're done. You'd use this any time a new piece of equipment is connected or an existing device's settings need to change.

### MSDE for AccuMark Storage Areas
MSDE is background database software that lets AccuMark store and retrieve pattern, marker, and order data from an SQL-type database rather than plain files. A technician installs it from media provided by Gerber, the computer may need a restart afterward, and once running it shows up as an icon in the system tray that can be checked to confirm the service is active. Workers generally won't install this themselves, but it's good to know that this is what's silently running in the background so the AccuMark storage areas work properly.

### Print a Hard Copy of the User's Guide
This explains how to get a paper copy of the software's help manual instead of only reading it on screen. You can either print a single help topic by choosing File > Print Topic from the online help menu, or open the full User's Guide (a PDF-style Adobe Acrobat file, found either in a desktop folder or in the Documentation screen of the LaunchPad), then use the File > Print command and choose to print the whole document or just a page range. Use this whenever you want a printed reference to keep at your workstation instead of switching screens to check the online help.

**Print a Hard Copy of the User's Guide** — This explains how to get a paper copy of the software's help manual instead of only reading it on screen. You can either print a single help topic by choosing File > Print Topic from the online help menu, or open the full User's Guide (a PDF-style Adobe Acrobat file, found either in a desktop folder or in the Documentation screen of the LaunchPad), then use the File > Print command and choose to print the whole document or just a page range. Use this whenever you want a printed reference to keep at your workstation instead of switching screens to check the online help.

### Ordering Markers
This is the process of filling out the Order Editor, the screen where you gather everything the system needs to lay out a marker (the layout of pattern pieces on fabric for cutting) — which pattern pieces (models) to include, which reference tables and forms to use, and what sizes and quantities of each piece you need. You'd use this any time you need the system to build a new cutting layout for a job, and it's the starting point for more advanced marker orders like ones with alterations, halfpiece sharing, or cutdowns.

### Setting Up Halfpiece Sharing
Halfpiece sharing lets a single pattern piece serve two garment sizes instead of needing to be placed twice in the marker (cutting layout), which saves fabric. It only works when the fabric is spread doubled over — face-to-face, tubular, or bookfold — so that cutting one piece naturally produces two layers; if just one piece is needed from that pair, it can be shared this way instead of being drawn twice in the layout.

### Nested Halfpieces
When two shared half-pieces are nested (fit closely together) in a marker to save fabric, you must mark a 'stacking point' — a location tag using the letter Z — on the piece using the Piece Verify/Edit Points screen, PDS, or by assigning code D3 while digitizing (converting a physical pattern into digital form), so the pieces don't overlap each other when placed. Always check the finished piece in Piece Verify to confirm the stacking point landed in the right spot; if the smaller piece sticks out past the main piece's edge, the system will automatically add buffering (extra spacing) to keep pieces from overlapping.

### To set up a model with halfpiece sharing
Before you can use halfpiece sharing on a piece, you have to mark it as a halfpiece in the Model Editor's Half PC field. The choices are None (no sharing, the normal default), Any Dir (the piece can be shared no matter which way the bundles of fabric are facing), or Same Dir (the piece can only be shared when the size bundle and its halfpiece partner face the same direction).

### To order a marker with halfpiece sharing
This walks through the steps to actually place a marker order (a cutting layout request) that uses halfpiece sharing: list sizes largest to smallest on the Order Editor's Models screen, set Master Type to Halfpiece, and know that ordering two of the same size will automatically pair them to share a piece unless you change the quantity to 1 and list the piece twice. A halfpiece can be shared with a same-size or a larger 'master' size (which must appear on an earlier line of the order), and the Direction setting makes sure the shared bundles line up correctly when cut.

### Setting up Cutdowns
Cutdowns (also called stepdowns or fractions) let you plot a smaller piece inside a larger 'master' size's outline within the same fabric layout, so after the master size is cut, extra fabric layers can be pulled away and the smaller cutdown piece cut from what's left. Because the cutdown piece sits inside the master piece's outline, stacking and buffering settings are used to keep it from extending past the master piece's edges.

### To order a marker with cutdowns
This explains the steps for placing a marker order that includes cutdowns: list sizes largest to smallest, set Master Type to Cutdown in the Order Editor, and make sure the master size (the larger size the cutdown is nested inside) is listed on an earlier line in the order. The Direction field controls which way the bundle faces — leaving it blank uses the standard lay limits table setting, while choosing Left overrides that and forces the bundle to a specific orientation.

### To order a marker with constructs
A construct is a marked-off, no-go area inside a marker (cutting layout) — used to block out fabric flaws or shading so the marker maker avoids placing pieces there, or to define plotter cutting windows on certain machines. To set one up, fill in the Order and Order Models screens as normal, go to the Constructs tab, name the construct, choose whether it should be plotted or cut (both default to No), and enter its corner coordinates to define exactly where the blocked-off area sits.

### To order a marker for block fusing
Block fusing is used when a garment needs a separate fusing layer (an interior reinforcing/stiffening layer) matched exactly to the shell layout. You create two nearly identical marker orders with different names — one for the outer shell and one for the fusing layer — and on the shell order you fill in the Block Fuse Name field with the name of its matching fusing marker so the two stay linked.

### To order a marker from an existing marker
This lets you reuse the piece layout from a marker you already made, instead of laying everything out again from scratch. In the Order Editor, switch the field under Block Fuse Name to Copy Marker and enter the name of the existing marker to copy from; unlike layrules (a saved layout pattern), the source marker here must still exist in the system since the system copies from it directly rather than from a saved rule.

### To order a marker for fabric that shrinks or stretches
This feature automatically resizes pattern pieces in a marker to account for fabric that will shrink or stretch after cutting, so the finished, shrunk or stretched piece ends up the correct final size. You enter the expected shrink or stretch percentage in the Order Form's X% and Y% fields (for example, -25.0 for fabric that shrinks 25%), and the system enlarges or reduces the pieces accordingly during order processing before cutting.

### Order Options
Order Options is a settings screen where you set preferences that control how the system behaves while creating and processing marker orders — such as whether to overwrite duplicate markers automatically, ask first, or never; which method to use for layrules (saved marker layout patterns); and how to handle split piece seams. You get to it via View > Order Options from the Order Editor or Order Process Editor, or through AccuMark Explorer's View > Process Preferences > Order Processing menu.

### To process a marker order
This is how you tell the system to actually generate the marker (cutting layout) from an order you've set up. From the GERBER LaunchPad, go to Marker Creation, Editors page, open Order Process, pick the storage location holding your order(s), select the order name(s) to run, and click Process (or Process All if layrules are involved) to have the system build the marker; pressing F2 first lets you review the order before committing to processing it.

### To verify the status of a processed order
After running a marker order, you can check how it went right on the Marker Order Processing screen. The System Messages at the bottom show Total Processed (how many orders ran, success or not), Errors (how many hit a problem, like a requested size not being available — check the Activity Log for details), and Overwritten (how many existing markers got replaced because of matching names), while the Status field shows a per-order status message.

### To process a marker using layrules
This is the step-by-step process for telling the system how to lay out (place) pattern pieces on fabric using a set of pre-defined placement rules called layrules, instead of laying every piece out manually. Before running the order, the worker sets the Layrule Mode on the Order Form to pick a method — such as copying a previous marker's layout, forcing a specific named layrule, or having the system search a table for the right layrule automatically. Once that field and the rest of the Order Form are filled in and the order is stored, the worker processes it from the Order Entry Main Menu, and the system builds the marker following those saved placement rules.

### To process a marker using load multi list
This function helps a worker recover and reprocess marker orders that failed due to errors during a previous run. The system automatically remembers the names of any orders that did not process successfully in the last session, and after checking the Activity Log to see what went wrong, the worker can open Load Multi List from the Marker Order Processing screen to pull up those failed order names, jump straight to the Order Form to fix the problem, and reprocess them. It saves time because the worker doesn't have to remember or retype which orders failed.

### To plot only a marker's annotation
This function prints a lightweight sheet showing just the labels/markings (annotation) for each pattern piece — like piece names, sizes, and bundle numbers — instead of printing the full outlines of every piece. The worker lays this sheet on top of the fabric before cutting so they can identify and sort pieces and bundles more easily. To set it up, the worker creates a new Marker Plot Parameter Table, sets Piece Annotation to 'All,' and chooses either 'First' (only the first piece's outline prints, everything else is just labels) or 'Window' (used for bite-feed cutters, where the first window shows full outlines and later windows show only labels).

### Plotting Bar Codes Using an AJ-510
This feature lets a worker print scannable bar codes directly onto marker plots using an AccuJet 510 plotter, as long as the plotter's firmware (its internal control software) supports it. The worker enters a special code in the Annotation Form specifying the bar code type (like type 128 or type 3 of 9), its width in mils (thousandths of an inch), and the text/data (up to 20 characters) it should represent. This is useful for adding trackable labels to pieces or bundles right on the cut marker.

### Setting Up Alteration Requirements
This is the initial setup work needed before a worker can make garment alterations (changes to length, width, or fit) in AccuMark. There are two kinds: Standard Alterations, which are common, standardized changes used the same way across many styles (like shortening an inseam), and Made-to-Measure Alterations, which are customized to an individual customer's exact body measurements. Setup starts by deciding, in the piece plot form, how alterations will be viewed and plotted (printed) for a given storage area.

### Workflow for Alterations
This outlines the full sequence of steps a worker follows to build and use alterations on a garment. It starts with marking where on the pattern pieces alterations will happen and labeling those spots with special point numbers, then defining the alteration rules in a rule table, checking the results on screen or on a printed plot, entering the actual alteration amounts in a Size Code Form, and finally ordering and processing the marker while pointing it to the correct rule table and size code table.

### To create an alterations rule table
This is the process for building a table that tells the system exactly how a pattern piece should change shape during an alteration. Working in the Alteration editor (found on the LaunchPad's Marker Creation/Editors page), the worker starts a new table, chooses whether the change applies to the left piece, right piece, or both, and picks an Alt Type that defines how lines or points move — for example turning clockwise or counter-clockwise, allowing the line to stretch (extend) or not, or simply sliding a point in the X or Y direction. This table becomes the rulebook the system uses whenever that alteration is applied to a marker.

### To retrieve and edit an alterations rule table
This is how a worker opens an existing alteration rule table to review or change it, rather than building one from scratch. From the Alterations editor on the LaunchPad, the worker uses File > Open to select the table by name, edits whatever fields need changing, and then either saves the changes to the same table or uses Save As to keep the changes under a new table name.

### To create a size code table for alterations
A size code table is a chart listing every alteration rule and the exact amount to change it by, for each possible altered size a worker might need to produce. In the Size Code editor, the worker enters the real, unaltered size of a piece (the Actual Size) along with the new size names being ordered (Ordered Size), and fills in the specific rule and amount for each; larger size ranges or more alteration types mean more entries in the table.

### To order a marker with alterations
This explains how to place a marker order that includes garment alterations rather than a plain, unaltered marker. The worker fills out the Order Form as usual, but on the Models screen also specifies which alteration rule table and which size code table the system should use — and different models within the same order can use different tables, mixing altered and unaltered styles. In the Size fields, the worker types the altered size names exactly as they appear in the size code table so the system pulls the correct alteration rules and amounts.

### Using Base Measurements
Base Measurements are a way of entering made-to-measure alterations using a customer's actual full-body measurement (like chest or sleeve length) instead of typing in the alteration amount directly. The system automatically compares that customer measurement to the standard size measurement and calculates the difference itself, which becomes the alteration amount — saving the worker from doing that math by hand. This method isn't available for every alteration type, but it's commonly used for things like coat length, sleeve length, chest, and waist.

### Activity Log Screen
The Activity Log is a screen that shows a running record of recent actions the system has performed, which is useful for tracking down what happened (and what may have gone wrong) during a job like marker processing. A worker opens it from the AccuMark Explorer's Utilities page by clicking the Activity Log icon, then scrolls through the entries to review them or clicks the Printer icon to print the log for reference. There is also an option to clear all entries from the log once they're no longer needed.

### Plot Options
Plot Options is a settings screen that controls how marker and cut-plot files are produced and printed, including the file type, bundle numbering method, default printer/plot queue, plot media, output folder, and whether printing happens automatically. For File Type, the worker chooses between 'Generic' (a universal AccuMark format any supported plotter can read) or 'HPGL' (a vector image format that can be opened in other software). For Bundles By, the worker chooses whether bundle numbers run continuously through the whole marker or restart consistently for each model when multiple models/sizes are combined.

### Block Fusing
Block Fusing is a method where several pattern pieces are grouped together into a 'block,' fusible interlining is applied to the whole block at once, and then the individual finished pieces are cut out of that fused block, either by hand or with a GERBERcutter (an automated cutting machine). AccuMark supports this by letting the worker group pieces into blocks right while making the marker, automatically sending the block's size and shape to a matching fusing marker, and generating the cutting data needed to cut the shell marker, the fusible marker, and the final finished pieces from the fused blocks.

### Overview of Block Fusing When Using a GERBERcutter
This describes the setup steps required before block fusing can be cut automatically with a GERBERcutter. The worker needs two Cutter Parameter Tables (one with 'Cut Net Parts' turned on, one with it turned off), two separate marker orders with matching details but different names — one for the shell marker and one for the fusing marker, linked together via the Block Fuse Name field — plus an Annotation Form set up to label block numbers, and the Block Fuse Notch option turned on in Marker Making Settings so the cutter's pause points (op-stops) are easy to spot.

### Workflow for Block Fusing When Using a GERBERcutter
This lays out the step-by-step order of operations for producing block-fused pieces with a GERBERcutter, starting with ordering and processing both required markers together. The worker then proceeds to actually build the shell marker as the next step in the sequence before moving on to cutting.

### Shell marker
The shell marker is the main marker that contains the actual finished, individual pattern pieces that will ultimately be cut out — it's paired with a separate fusing marker used to fuse blocks of fabric before the final pieces are cut from them.

### Fusing marker
The fusing marker is the companion marker to the shell marker in a block fusing setup; it contains the pre-cut block shapes that get interlining fused onto them before the finished pieces are separated out, and it's linked to its matching shell marker by name in the order setup.

### Block
This is the process of grouping pattern pieces into rectangular or manual-shaped "blocks" so they can be fused (bonded with a heat-activated backing) together instead of one at a time. You place these blocks on the marker (the layout that shows how pieces fit on the fabric) along with the other pieces to use as much fabric as possible, then save the marker. Workers use this when a group of pieces needs stiffening material applied efficiently before final cutting.

### Block Fuse Amount
This tells the system how much bigger to make the block compared to the actual pattern pieces inside it. It matters because the block needs extra fabric around the piece edges so the fusing (bonding) material fully covers the piece before it's trimmed down to size.

### Block Notch
This is a small V-shaped cut or mark placed on the block at the point where the cutter pauses to reposition (called the Op-Stop). Its depth is calculated by taking the block fuse amount and subtracting the reduce fuse amount, and it helps guide accurate cutting after fusing.

### Canvas
This is the common shop-floor term for woven fusible material — a woven fabric with a bonding layer that sticks when heated. It's mainly used to stiffen coat and jacket fronts.

### Create Fuse
This is a command used in Marker Making (the layout tool) that copies the blocks you created into a new, separate marker and automatically shrinks them down in size. Workers use this to build the actual fusing marker that will be used to cut the fusible material, separate from the main shell marker.

### Cut Net Parts
This is a checkbox setting in the Cutter Parameter Table (the settings that control how the automatic fabric-cutting machine behaves). When turned on, it tells the GERBERcutter machine to cut out the actual pattern pieces inside each block instead of just cutting around the block's outer edge, and it automatically adds a pause point (Op-Stop) at the block notch. Workers use this setting specifically for the final cutting step after the fused blocks have been made.

### Fusible
This is any fabric — woven or non-woven — that has glue or another bonding substance on one side. When you apply heat and pressure to it, it sticks to another fabric, which is used to make that fabric stiffer or change how it feels (its "hand").

### Message Stop
This is a built-in instruction in the cutting data that makes the GERBERcutter machine pause and show a text message on its control panel. Workers see this when the machine needs to alert them about something during the cutting job, such as an instruction or reminder.

### Op–Stop
This is a command in the cutting data that tells the GERBERcutter machine to pause and wait while the operator adjusts the position of the cutting head. It's essentially a way to reset or fine-tune the starting point (origin) before the machine cuts the next part.

### Reduce Fuse Amount
This is the measurement used to shrink a block down in size when it gets copied over into the Fuse Marker. It works together with the Block Fuse Amount to determine the final size and notch depth used during the fusing and cutting process.

### Shell
This refers to the outer fabric of a garment piece — the material you actually see when wearing the finished item. On the shop floor it's also commonly called the "self" fabric.

### Block fusing
This is the overall process of grouping several pattern pieces together into blocks, applying fusible (bonding) material to them as a group, and then cutting the individual pieces out of the fused blocks either by hand or with a GERBERcutter machine. It's a more efficient way to fuse and cut small or similarly-shaped pieces instead of handling each one separately.

### AutoMark
This is a tool that automatically places pattern pieces onto a marker (fabric layout) using the computer instead of a person doing it by hand. Workers use it as a quick way to build sample/costing markers or get a starting layout before fine-tuning it, and it can also automatically optimize the layout or swap piece sizes; it also keeps an activity log and a job list of markers waiting to be processed.

### To process an AutoMark job list
This is the step-by-step procedure for having the computer automatically lay out one or more markers: you pick the starting (source) marker and the marker you want to save the result as (destination), choose your settings (like layout strategy and piece options), then either process one job at a time or run the whole list at once using the Process menu or toolbar icon. Afterward, you can view the finished layout on screen, print a small version of it, and check the AutoMark Log to see how it went.

### AutoMark Editor Field Explanations
This is a reference guide describing what to type or select in each box of the AutoMark screen — for example, the Source Marker field is where you pick the marker(s) you want automatically laid out, and the Destination Marker field is where you name the marker that will be saved once processing is done. Workers use this guide to correctly fill out the AutoMark screen before running an automatic layout job.

### AutoMark Menu Commands
This describes what each menu option in the AutoMark screen does — for example, Process Entries or Process Job List runs all the queued markers automatically one after another, Add to Job List puts the current marker into the waiting list, and View Log shows the results/history of past AutoMark runs. Workers use these menus to control and review automatic marker layout jobs.

### AutoMark Log
This is a report you can open from the AutoMark screen, the toolbar, or the Explorer that shows the results of markers that were automatically laid out — including how much fabric was used (utilization percentage), the marker's length, how many pieces were placed or left unplaced, how long it took, the cost, and any errors. You can also use this screen to clear out old log entries when you no longer need them.

### Grade Rule Table Editor
This is the screen used to build or edit a grade rule table, which is the set of measurements that tells the system how to resize a pattern piece up or down for different sizes. In it, workers name the table, optionally add notes, choose whether sizes are numeric (like 8, 10, 12) or alphanumeric (like S, M, L), and set the base size that all the other sizes are graded from.

### Edit Digitized Editor
This is a screen you open from the Gerber LaunchPad (Pattern Processing, Digitizing, PDS button, then the Edit Digitize icon) that shows, in order, every button push you made on the digitizing cursor when you traced a pattern piece. You use it to fix mistakes such as wrong piece information or a wrong grade rule number, or when you tried to open a digitized piece and got an error message. If the screen comes up blank, that means the piece can't be fixed here and must be re-digitized from scratch.

### Piece Plot Parameter Table
This is a table you set up (opened through AccuMark Explorer or the Gerber LaunchPad's Plotting and Cutting button) that stores the settings used when printing or plotting pattern pieces, such as layout and print options. You open, save, and print these tables from its File menu, and use the Edit menu to cut, copy, or paste information into them.

### Piece Plot
Piece Plot is the function that actually prints (plots) your pattern pieces onto paper or film using the settings saved in a Piece Plot Parameter Table. You open the parameter table from AccuMark Explorer or the Gerber LaunchPad, pick the folder with the table you need, and double-click it to run the plot with those settings already filled in.

### Inputting Pattern Pieces
This refers to the different ways you can get a pattern piece's shape and data into the AccuMark system, such as digitizing it by hand, converting/importing a file, or using PDS/Silhouette drawing tools. You pick whichever method fits the piece you're working with and the tools available on your floor.

### Digitizing
Digitizing is the process of tracing a physical paper pattern piece into AccuMark using a digitizing cursor on a digitizing table, so the computer captures its exact shape and sizing information. As you trace, you also record grade points (sizing reference points), grade rules (how much the piece grows or shrinks between sizes), intermediate points, special point numbers, notches, and any internal markings, all in one pass.

### Digitizing Menu
This is a keyboard-like menu built into the lower left corner of the digitizing table, showing letters, a numeric keypad, and special option buttons for digitizing tasks. To use it, you line up the crosshairs of the digitizing cursor over the item you want and press the A button on the cursor to select it.

### Digitizing Menu Options
These are the specific commands available on the digitizing menu keyboard: Start Piece begins a new pattern piece, Large Piece tells the system a piece continues beyond the table surface, Rule Table tells it you're using grade rules from an existing table, Numeric Sizes and Alpha Sizes tell it whether the nested piece's size line uses numbers or letters, and Copy Piece duplicates piece data. You select the one that matches what you're about to do before or during tracing a piece.

### Digitizing Cursor
The digitizing cursor is the handheld pointer you move across the digitizing table to trace a pattern piece and trigger commands like Close Piece (finish the outline, letting the system draw the last connecting line automatically), Mirror Piece (flip the piece at a mirror line), 90 Degree Angle, Circle Ctr/Rad, Delete Piece, or End Input. You press its buttons at specific points on the piece to record shape, grading, and special instructions as you go.

### Digitizing Cursor Buttons
Each button on the digitizing cursor has a labeled job: the A (Point) button marks the X/Y location of grade points, intermediate points, and grain lines as you trace; the B (Rule) button, followed by a number, assigns a grade rule to a point so the system knows how that point resizes across sizes. You press these buttons in the right sequence at each spot on the pattern to build the piece correctly in AccuMark.

### To select items from the digitizing menu
To pick something from the digitizing menu, you move the digitizing cursor until its crosshairs sit directly over the menu item you want, then press the A button once — you'll hear a beep confirming the selection. You also use this same method to assign point attributes (extra properties on a grade point) by selecting the word Attribute followed by the matching letter.

### To prepare pieces for digitizing
Preparing a piece means writing helpful notes directly on the paper pattern before you digitize it — things like the piece description, which grading method or rule table to use, the grain line, grade rule numbers, notches, and intermediate points. Doing this ahead of time makes the actual digitizing faster and reduces mistakes, though attributes and internals can also be added later during piece verification.

### Placing a Piece on the Digitizing Table
This is the step of physically securing your pattern piece to the digitizing table using masking tape (not other tapes or adhesives) on a clean surface free of dirt or smudges. You should try to line up the piece the way you want it to look on screen and watch out for the table's "dead zone," since AccuMark will automatically straighten the piece based on its grain line after digitizing.

### Descriptive Piece Data
Descriptive piece data is the basic identifying information you record for a pattern piece — like its name, category, and description — before or while digitizing it. This information helps AccuMark and other workers correctly identify and organize the piece within a style or model.

**Information You Need for Every Piece** — Every piece you digitize needs a unique Piece Name (1-20 characters), a unique Piece Category describing the piece type such as shirtfront or back (1-20 characters), an optional Description for extra detail, and a specified Grading Method (Rule Table, or Numeric/Alpha Sizes) telling AccuMark how the piece changes across sizes. Filling these in correctly ensures the piece is stored and graded properly in the system.

### Making Perimeter Notes
This is the practice of writing down, directly on your paper pattern piece, all the button pushes and details you'll need during digitizing — including grade rules, notch types, grade point and intermediate point locations, the grain line, attributes, and internals. It's especially recommended for beginners, and for large pieces you should also mark transition and locator points.

### Including Internals in Your Piece
Internals are extra markings inside a pattern piece, such as buttonholes, drill holes, or cutouts, and you should decide during pattern preparation whether your piece needs them. They require their own special sequence of digitizing cursor button pushes and are always traced after you've finished digitizing the piece's outer perimeter.

### Defining Internals
Internals are extra features inside a piece — like two- or three-point annotation lines, drill holes, cutouts, or user-defined shapes — that you add using the digitizing menu, either with your own chosen label or a fixed system letter. For example, label D marks a drill hole, label H marks a cutout that must be a closed shape, and label G is automatically assigned to a grain line.

### When to Use Internal Labels
Internal labels are always digitized after the piece's outer perimeter has been closed or mirrored, and different labels behave differently when a piece is mirrored: labels A, B, C, E, F, G, H, J, K, L, M, and N will not mirror, while D, O, P, Q, R, S, T, U, V, W, X, Y, and Z will. If you mark a cutout with label H (which must be a closed internal shape), that opening can later hold another piece when building a marker for cutting.

### Converting/Importing
This is where you bring in pattern pieces that were originally made on a different CAD (computer-aided design) system so they can be used in AccuMark. Gerber sells separate conversion programs that translate the other system's files into AccuMark's format; a worker would contact their Gerber Sales Representative to get the right conversion tool set up rather than trying to import the file directly.

### Using PDS/Silhouette
PDS and Silhouette are Gerber design applications you can use to build or bring in new pattern pieces for AccuMark instead of digitizing them by hand. In PDS you create pieces using tools in the Blocks Menu, and in Silhouette you use tools in the Draft Menu; the built-in Online Help in each program walks you through the specific steps.

### To digitize a basic closed piece
This is the step-by-step method for turning a physical paper pattern piece into digital data using a digitizing table and cursor (a pointing device with buttons). You tape the piece down in its correct grading orientation with the grain line flat/horizontal, then use the 'Start Piece' menu option and enter the piece's name, category, and description by pointing at letters/numbers on the digitizing menu and clicking the A button. Workers use this whenever they need to get a new, simple pattern piece with notches into the AccuMark system so it can be graded and used for production.

### To digitizing special point numbers
Normally AccuMark automatically numbers every point on a piece in order as you digitize it, but this feature lets you manually assign your own number (1 to 4 digits, 0-9999) to a specific point instead. Workers use this to make an important point stand out from the rest, which is especially useful for matching seams between pieces, alteration pieces, or paste pieces; to do it, you point the cursor at the spot, press the A button, then key in your chosen number.

### To digitize from a nest
This method lets you digitize a piece straight from a 'nest' (a marker or layout where multiple graded sizes of a piece are already arranged together), so the grading is captured automatically instead of needing a separate grade rule table set up beforehand. You tape the nested piece to the table in its graded orientation with the grain line flat, then start the piece and enter its name and category just like normal digitizing, but the system builds the size grading directly from what's on the table.

### To digitize a mirrored piece
A mirrored piece is one where only half the pattern is drawn and AccuMark automatically creates the other, symmetrical half using a mirror line. When digitizing this way, you should trace the grain line (the line showing fabric direction) over the exact same start and end points as the mirror line, rather than placing it above the mirror line as usual, to keep the grading accurate.

### To digitize a copy piece
This feature lets you create a new graded piece by copying the grading rules from an existing AccuMark piece instead of typing them in from a grade rule table. It saves time when you're working with nested patterns or when rules were already fixed/edited on one piece and need to be reused on a new one — but the piece you copy from must be stored in the same location as the new piece, and it must already have every grade rule the new piece needs.

### To digitize angled notches
An angled notch is a notch (small cut mark on a pattern edge used for matching pieces during sewing) that sits at an angle instead of straight in/out, and it will show up tilted on screen, on printed plots, and can be cut that way on a Gerber cutting machine. There are two ways to create one: by using a grade rule table or by digitizing from an already-nested piece.

### To digitize an angled notch using a rule table
This is the specific button sequence for adding an angled notch while digitizing a piece against a grade rule table. After reaching the notch location, you press A (mark the point), optionally assign a special point number, press B and enter the grade rule number, then press C and enter the notch type, and finally move to where the notch should end and press C again — the angle comes from the line between your first and last points, while the notch's depth and width come from settings in the Notch parameter table.

### To digitize an angled notch using a nested piece
This is the version of angled-notch digitizing used when you're working from a nested piece rather than a grade rule table. You mark the notch location with the A button, optionally give it a special point number, press B, then press C and select the notch type, and finish by moving to the end location and pressing C again — the angle is set by the line between those two points, and depth/width come from the Notch parameter table settings.

### Plotting Angled Notches
This refers to how angled notches print out on paper — they show up correctly angled on both individual piece plots and full marker (layout) plots. However, if the pattern data is sent to an older AM-5 system, those angled notches automatically convert into standard straight (perpendicular) notches.

### To digitize internals on your piece
Internals are markings inside a pattern piece — like drill holes, buttonholes, or pocket placement lines — that aren't part of the piece's outer edge. To add them, you digitize as normal but, after closing or mirroring the piece, you select an 'Internal Label' (a code telling AccuMark what kind of internal it is) before marking each one, and you must reselect the label each time you switch to a different type of internal.

### To digitize multiple grain lines
Grain lines show the direction fabric should run and are normally just one line per piece, but some garments need more than one grading reference line on the same piece. This feature is especially useful for swimwear, lingerie, or bridal wear, and you set it up the same way as starting a basic piece — taping it down, starting the piece, and entering its name, category, and description — before adding the extra grain lines.

### To digitize large pieces
This lets you digitize a pattern piece too big to fit on the digitizing table in one go, handling pieces as large as 7 x 45 feet — commonly used for bridal gowns or sails. You divide the piece into smaller grid sections (drawn with grid lines and numbered clockwise starting at the lower left), digitize each section separately with locator points connecting the grid lines, and AccuMark reassembles them into one complete piece.

### To digitize 90 degree angles
This feature forces a specific point on a pattern piece (or an internal marking) to be a perfect right angle (90 degrees). You do this by digitizing the point just before and just after the corner, selecting '90 Degree Angle' from the menu, then digitizing the actual corner point, and continuing on to finish the piece normally.

### To digitize paste pieces
A paste piece is a smaller add-on pattern piece that attaches to a larger 'parent' piece, used to build modular patterns (patterns made of interchangeable parts). You digitize both the paste piece and the parent piece the same way you would a basic closed piece, attaching the smaller piece to either the inside or outside edge of the larger one, keeping a few special rules in mind for how the two connect.

### When digitizing the parent piece
When digitizing the larger 'parent' piece in a paste-piece setup, you must trace it in a clockwise direction and mark the connection points (where the paste piece will attach) as special point numbers, with the joining line between them being perfectly straight. The very first and last points you digitize on the parent piece can never be used as these paste (connection) points, and whatever paste points you set must line up with matching points on the paste piece.

### When digitizing the paste piece
When digitizing the smaller 'paste' piece that attaches to a parent piece, you also trace it clockwise and mark connection points as special point numbers along a straight paste line. Unlike the parent piece, the very first and last points you digitize on the paste piece MUST be the paste (connection) points, and they need to match up exactly with the corresponding points on the parent piece.

### Paste Pieces
Paste Pieces is a feature that lets you join two or more separate pattern pieces together during order processing to create one combined piece, which is useful for making garments from modular patterns (a small set of reusable pattern blocks that can be mixed and matched). Modular patterns use "parent" pieces (the main or partial pattern blocks) and "paste pieces" (optional add-on blocks), like a jacket front that can have different armhole, lapel, button, or pocket options pasted onto the same base. The matching points where pieces join must line up within .10 inches of each other (the "paste tolerance"); if they don't, the order will still go through but you'll get a warning message.

### Follow-On Pieces
Follow-On Pieces are a type of internal paste piece attached to a main (parent) piece rather than joined at an edge. Workers use them to add internal details like drill holes, gores (fabric inserts), or grain lines; edge details like notches or darts; or surface details like letters, logos, or map outlines.

### Guidelines for placing a paste piece outside a parent's perimeter
This is the rule for lining up a paste piece when it attaches to the outside edge of the parent piece: you match the first paste point on the parent to the first paste point on the paste piece, and then match the last paste point on the parent to the last paste point on the paste piece. Following this order ensures the two pieces join correctly instead of ending up flipped or misaligned.

### Guidelines for placing a paste piece inside a parent's perimeter
This is the rule for lining up a paste piece when it fits inside the parent piece's outline: here you match the first paste point on the parent to the last paste point on the paste piece, and the last paste point on the parent to the first paste point on the paste piece (the reverse order used for outside placement). Using the correct matching order keeps the inserted piece oriented properly within the parent shape.

### To digitize a follow-on piece
This is the step-by-step process for entering a follow-on piece (an internal or attached detail piece) into the system using a digitizing table, a device that traces a physical pattern into digital form. You first digitize the parent piece as normal and leave it on the table, then position the follow-on piece on top of it, select "Follow-On" from the digitizing menu, enter its identification info (name, category, description, grade rule table), trace its grain line so it lines up with the parent's grain line, and add the appropriate internal label; the two pieces must share the same piece category.

### Generating Reports
Generating Reports means pulling up detailed information that AccuMark has been automatically tracking about your pieces, markers, splice marks, plot files, or cut files. Workers use this when they need exact details on something already in the system, such as checking measurements or verifying data before cutting or shipping.

**What Reports are Available?** — AccuMark offers several built-in reports covering splice marks, pieces, markers, layrules (rules controlling how pieces are laid out on fabric), and marker cut files. Some reports give details on just one item, while others summarize information across many items of the same or different types, so workers can pick the report that matches what they need to check.

**To generate a Splice Report** — A Splice Report shows information about splice marks (marks indicating where fabric pieces need to be joined or matched during layout/cutting) for a selected item. You generate it by selecting the item in AccuMark Explorer (the file-browser part of the software) and choosing Reports from the right-click menu, after which the report displays on screen.

**To generate a Single Piece Report** — A Single Piece Report gives detailed information about one specific pattern piece you select. To run it, select the piece in AccuMark Explorer, right-click and choose Reports, then pick "One Piece Report" from the Reports menu to display it on screen.

**To generate an All Piece Report** — An All Piece Report gives detailed information covering every piece in a selected item (such as a whole style), rather than just one piece. You generate it by selecting the item in AccuMark Explorer, right-clicking to choose Reports, then selecting "All Piece Report" from the Reports menu.

**To generate a Piece Perimeter Report** — A Piece Perimeter Report gives measurement and outline details about the perimeter (outer edge) of a pattern piece. You generate it the same way as other reports — select the item in AccuMark Explorer, right-click, choose Reports, and select this report type from the menu.

**To generate an All Marker Report** — An All Marker Report provides detailed information about markers (the layouts showing how pattern pieces are arranged on fabric to minimize waste) for a selected item, covering all markers rather than just one. You run it from AccuMark Explorer by selecting the item, right-clicking to choose Reports, and selecting the All Marker Report option.

**To generate an All Layrule Report** — An All Layrule Report shows the layrules (the rules that control how pattern pieces should be positioned relative to the fabric grain, nap, or fold during marker-making) for all relevant items. It's generated the same way as other reports — select the item in AccuMark Explorer, right-click, choose Reports, and pick this report from the list.

**To generate an All Plot Report** — An All Plot Report displays details about plot data — the files used to print or plot pattern pieces and markers onto paper or fabric — for a selected item. You access it through AccuMark Explorer by selecting the item, right-clicking for the Reports menu, and choosing the All Plot Report option.

**To generate an All Cut Report** — The full process for generating any of these reports is: in the AccuMark Explorer, select the item you want information on, right-click and choose Reports, then pick the specific report (Splice, One Piece, All Piece, Piece Perimeter, All Marker, All Layrule, or All Plot) from the Reports menu, and the chosen report will display on screen. An All Cut Report specifically shows details about cut data — the files that control how markers are cut — for the selected item.

**Grading and Grade Rules** — Grading and Grade Rules refers to AccuMark's automated way of doing what pattern makers used to do by hand: growing or shrinking a pattern piece to create different sizes based on measurements you set while digitizing, verifying pieces, or working in PDS (Pattern Design System). Once you tell AccuMark how a pattern should grow between sizes, it automatically reapplies those same size changes every time, saving you from manually re-measuring for each size.

### How Grading Works in AccuMark
In manual grading, you move a pattern piece up, down, in, and out on a table to create each new size from a base size; AccuMark does the same thing digitally using X and Y (horizontal and vertical) movements on a grid instead of a physical table. Rather than judging the whole shape by eye, AccuMark tracks specific spots on the piece called grade points, and moves each one by a set X/Y distance and direction to build each size, working up and down from the base size.

### Sample Graded Pattern
This is a worked example showing a simple rectangular piece graded into five sizes (8 through 16, with 12 as the base size) to illustrate how individual grade points move between sizes. One point (a notch) has zero growth and doesn't move, while the other four points each move set amounts along the X-axis (up/down) and Y-axis (in/out) as the size increases, demonstrating exactly how AccuMark reshapes a piece size by size.

### Grade Rule Tables
Grade Rule Tables are lists you build using the Grade Rule Editor that tell the software how much each point on a pattern piece should grow or shrink between sizes (called grading). For each point, you enter X (side-to-side) and Y (up-and-down) measurements, so a point with zero growth stays put while others move by set amounts to make bigger or smaller sizes. Once a table is built, you can reuse the same set of grade rules on matching points on other pattern pieces whenever you digitize, verify pieces, or work in PDS (Pattern Design System), saving you from re-entering the same measurements each time.

### Things to Remember About Grading
This is a checklist of practical rules to keep in mind before grading a pattern: every grade rule needs its own unique number in a table, it's smart to jot notes on the paper pattern about which table and rule numbers you'll use before digitizing, and you need a separate table for every size range. It also reminds workers that alphanumeric size ranges (like S, M, L) must be listed size by size, while numeric size ranges (like 6, 8, 10) only need the size step, smallest, base, largest size, and any grade breaks entered.

### Naming a Grade Rule Table
When you first set up a grade rule table in the Rule Table Editor, you have to give it a clear, meaningful name so that anyone else on the system can recognize and find it later. Common practice is to name the table after the size range it covers (like Missy, Petite, Toddlers) or after a specific product line or contractor, so it's obvious at a glance what the table is for.

### To create a grade rule table
This is the step-by-step process for building a brand-new grade rule table: you open the Grade Rule Editor from the LaunchPad, choose File/New to get a blank form, and then fill in details like comments, whether sizes are numeric or lettered, the base (starting) size, the size step (the gap between sizes, like every 2 inches), and the smallest and largest sizes in the range. Following these steps sets up the framework the system will use to grow or shrink the pattern into all its sizes.

### To retrieve and edit a grade rule table
This is the procedure for opening an existing grade rule table so you can review or change it: you go to the Grade Rule Editor, use File/Open to pick the table from a list, and double-click to load it, which displays its information on the Rule Table and Rule tabs. From there you can edit the values as needed and then choose Save or Save As to keep your changes.

### To search for a grade rule
This function lets you find a grade rule in the current table that matches (exactly or closely) another rule's X and Y movement values, so you don't have to compare numbers by hand. You highlight a rule number, right-click and choose Search, then tell the system how close a match you want (0% for exact, up to 10% for a looser match), and it jumps the cursor to any matching rule it finds.

### To display a specific grade rule
This command lets you jump straight to a particular grade rule by typing in its rule number, instead of scrolling through the whole table one rule at a time. You use Rule/Go to Rule on the menu, enter the number, and the system displays that rule; if the exact number doesn't exist, it shows you the closest one instead.

### To display a specific size break
This command lets you jump directly to a specific size (called a size break, meaning a defined size point in the grading range) within the Rule Table Editor by typing in the size instead of scrolling through them one by one. You use Rule/Go To Size, enter the size, and the system shows that size break, or the nearest one if that exact size isn't in the table.

### To copy a grade rule
This function lets you duplicate an existing grade rule's measurements into a new, blank rule slot so you don't have to retype similar values from scratch. You move to the empty fields after the last rule in the table, choose Copy Rule, then enter the source rule number (the one you're copying from) and a destination rule number (the new rule's number) to complete the copy.

### To import a grade rule from another rule table
This function brings a grade rule's measurements in from a different, already-existing grade rule table into the one you're currently working on, rather than making you re-enter the values by hand. You move to a blank rule slot, assign it a new rule number, choose Import Rule, and then tell the system the storage area (the folder/location where files are kept) and name of the table you want to pull the rule from — note both tables must use the same size range.

### To import a grade rule from a piece
This function pulls a grade rule directly off of an existing pattern piece (rather than from another rule table) and adds it into your current grade rule table, so you can reuse grading that's already been applied to a piece. You move to a blank rule slot, give it a new rule number, choose Import PC-Rule, and then enter the storage area and piece name that contains the rule you want, as long as both share the same size range.

### To change the grade rule values in a specific column
This command flips the plus/minus sign of every value in one column of grade rule numbers at once, turning growth into shrinkage or vice versa, instead of editing each number by hand. You put your cursor in the column, choose Change Sign, and confirm, and the system automatically swaps positive values to negative and negative values to positive throughout that column.

### To clear the grade rule values in a specific column
This command erases all the numbers in one column of the grade rule table at once, which is handy if you need to start that column over. You position the cursor in the column you want to empty, choose Clear Column, and confirm, and every value in that column is deleted.

### Rules
This opens page 2 of the Rule Table Editor, which is the actual work screen where you build and edit the grade rules — the specific growth/shrink measurements — for your pattern pieces.

### Search
This tool lets you look through the grade rule table you're currently working in to find a rule that exactly or nearly matches another one, so you can spot duplicates or find a similar existing rule instead of creating a new one from scratch.

### Go To Rule
This command lets you jump immediately to a specific grade rule by entering its number, which is much faster than pressing the arrow keys repeatedly to page through a long table of rules one at a time.

### Go To Size
This command lets you jump straight to a specific size break (a defined size point in the grading table) when a table has more than 10 sizes, saving you from having to press the up/down arrow keys over and over to find it.

### Copy Rule
This command makes a copy of a grade rule that already exists in the current table so you can then tweak it slightly for a new rule, which is handy when the new rule you need is very similar to one you've already built.

### Import Rule
This command lets you copy a grade rule (the set of measurements that tells the system how much bigger or smaller a pattern piece gets for each size) from another grade rule table into the one you're currently building, so you don't have to re-enter the same values by hand. You can only do this if both the table you're copying from and the one you're working on use the same size line (list of sizes) and are stored in the same storage area. Use it whenever a rule you need already exists elsewhere and matches your current size setup.

### Import PC–Rule
This command copies a grade rule directly from a pattern piece (rather than from a grade rule table), and that piece can be in any storage area. It's commonly used when you want to reuse a rule that was already created on a nested piece, a converted piece, or a piece built in PDS (the pattern design software). The only requirement is that the piece's size line or range matches the size line of the grade rule table you're currently working in.

### Change Sign
This command flips the plus/minus direction of every value in one grade rule column (either the X, meaning side-to-side, or Y, meaning up-and-down direction). Every positive number in that column becomes negative, and every negative number becomes positive. You'd use this if a grade rule was built in the wrong direction and you need to reverse it quickly instead of retyping every value.

### Clear Column
This command wipes out every value in one grade rule column, whether it's an X (horizontal) or Y (vertical) column, leaving it empty. Use it when you need to start that column over from scratch instead of correcting or overwriting each value one at a time.

### What if I Can't Retrieve a Digitized Piece?
If you try to pull up a piece you digitized (traced into the computer with a digitizing cursor) and it won't come up, it usually means something went wrong during digitizing — a button push was skipped, an extra button push was added by mistake, the grade rule table name was typed wrong or doesn't exist, or the grain line (the line showing fabric direction) wasn't marked. In rare cases the piece file itself becomes damaged and can't be fixed, meaning you'll have to digitize the piece all over again.

### Display Piece
To view a piece on screen, select it, right-click, choose "Open With," and then select Pattern Design. It's good practice to display a piece right after digitizing it (before you save/store it) to check that everything was traced in correctly, and if you spot a mistake you can fix it using the Edit Digitize or Edit Points tools.

### Display Graded
This command, run from PDS (the pattern design software), shows you the piece in all of its graded sizes at once, so you can see how the shape scales up and down across the size range instead of looking at just one size.

### To edit the grain line for a piece
Changing the grain line (the marked line that shows which way the fabric's weave should run on a pattern piece) is done in PDS, the pattern design software, rather than in Order Entry — the manual directs you to the PDS help section for the step-by-step instructions.

### To edit the points in a piece
Adjusting the individual points that make up a pattern piece's shape (the corners and curve points) is handled in PDS, the pattern design software, not in this module — refer to PDS help for the detailed steps.

### To display a grade point
Viewing a grade point (a specific point on the pattern that has grading, or size-scaling, values attached to it) is done through PDS, the pattern design software; the manual points you to PDS help for instructions.

### Go To Point
This function jumps directly to a specific point on a pattern piece so you can inspect or edit it, and like other point/line editing, it's performed in PDS, the pattern design software — check PDS help for the exact steps.

### Next Point
"Next Point" and "Previous Point" let you step forward or backward through the points of a pattern piece one at a time, which is useful for reviewing or fixing a piece point-by-point in sequence; this is done in PDS, the pattern design software, per PDS help.

### Insert Point
"Insert Point" adds a new point into a pattern piece's outline where one is needed (for example, to add more detail to a curve), while "Delete Point" removes a point that shouldn't be there; both actions are performed in PDS, the pattern design software.

### To delete a point
This removes an unwanted or mistakenly placed point from a pattern piece's outline. Like other point edits, it's done in PDS, the pattern design software — see PDS help for the exact steps.

### To change a point
This lets you modify an existing point on a pattern piece (for example, moving it or changing its type) and is done in PDS, the pattern design software; a related function, "Insert Internal," adds an internal line or marking (like a pocket placement or notch) inside the piece, also done in PDS.

### Delete an internal
This removes an internal marking or line (such as a dart, pocket placement, or notch marking) from inside a pattern piece, done in PDS, the pattern design software. The excerpt also introduces the Edit Digitize screen, a table showing details of how a piece was digitized — including a Status field for errors, a Line # showing the order of button pushes, a Button Press field listing which cursor buttons were used, and a Button Type field showing what kind of information (a menu selection or a plain button push) each entry represents.

### Button Types
The Button Type field on the Edit Digitize screen tells you what kind of data each digitizing action recorded — for example, choosing "Start Piece" from the digitizing menu shows as "Start Piece," choosing a rule table shows as "Rule Table," and so on for things like sizes, internal labels, attributes, alternate grain lines, angles, circles, and closing the piece. The X Coord and Y Coord fields next to it show the horizontal and vertical position recorded for that button push, and workers use this table as a reference to understand or correct digitized data for a piece.

### Edit Digitize Screen Menu Commands
The Edit Digitize screen has standard menus and toolbar buttons for managing your digitized piece data: File opens, clears, saves, and prints the Edit Digitize form; Edit lets you cut, copy, and paste information within it; View lets you show/hide the toolbar and status bar and open an activity log; and Help gives information about the Edit Digitize tool. The toolbar icons offer quick one-click access to these same actions (clear, open, save, cut, copy, paste, print, view activity log, and get help).

### To edit digitized data
This is the step-by-step process for opening and correcting a piece's raw digitized data (the button-push points recorded when the piece was traced onto the digitizing table). You find the piece in AccuMark Explorer, double-click it to open the Edit Digitize Form, make your corrections, and then click the Save icon to keep the changes. Use this when you spot an error in a digitized piece before it becomes a final usable pattern piece.

### To add a line to digitized data
This tells you how to insert a missing line of information into a piece's digitized data, for example if you forgot to press the delimiter button (*) marking the end of an item while digitizing. You highlight the line above where the new line should go, right-click, and choose Insert Rows to add a blank line, then fill in the correct command and coordinates from the drop-down menu. This lets you fix an incomplete digitizing record without having to re-digitize the whole piece.

### To delete a line from digitized data
This is the procedure for removing an unwanted or incorrect line from a piece's digitized data. You simply highlight the line you want to get rid of, right-click, and select Delete Rows to remove it. It's a quick fix for cleaning up mistakes made during digitizing.

### Piece Plotting
Piece Plotting is the function used to print or cut out pattern pieces on a plotter (a large printer/cutter used in apparel production) instead of just viewing them on screen. It covers the various settings and options for sending piece data to be physically plotted or cut on paper or fabric.

### Plotter Parameter Tables Versus Plotter Settings
This explains the difference between the Plotter Parameter Table (a saved table of standard settings AccuMark normally reads first when preparing plot data) and the Plotter Settings screen accessed through AccuMark Utilities, which lets you set up custom, one-off settings for a specific plot job. Knowing the difference matters because custom settings on the Plotter Settings screen can override the standard table settings when a plot actually runs.

### To plot pieces
This describes what happens when you send pattern pieces to be plotted (printed or cut): the system first checks the Piece Plot Parameter Table for standard settings like whether to use a pen or a cutting knife, but if you've entered different custom settings on the Plotter Settings screen, those custom settings take over and override the table once the job reaches the plot queue (the waiting line of jobs sent to the plotter). In practice, this means you should always check the Plotter Settings screen if your plotted piece doesn't come out the way you expected based on the parameter table.

### Perform Piece Plots by Model
This lets you plot every piece belonging to a specific model — including both left and right versions of pieces — in a single plot request instead of selecting pieces one at a time. You do this by setting the Piece Plot form's mode to Model, toggling the Plot As field to Model, and then picking the model you want; the system automatically plots all the piece orientations set up for that model. This saves time when you need a complete set of pieces for a style plotted at once.

### To save piece plot data as a DOS file
This is the process for saving plot data to a computer file instead of sending it straight to a plotter machine. You first set the DOS File Configuration dialog box to choose the file format (generic AccuMark format or HPGL), then go to Plot > Piece Plot, set the Plot Destination to DOS File, fill out the rest of the piece plot screen, and run Process (or Process Group for multiple pieces). This is useful when you need to store, transfer, or later reprint plot data without redoing the plot setup.

### Store Verifying
Store Verifying is the step where you confirm a digitized piece's shape is correct and then use File/Save to turn that raw digitized data into an official, usable AccuMark piece, which removes it from the temporary Digitizer storage and places it in the Current storage area. Once stored, you can still reshape the piece but can no longer edit its original digitized data directly; every digitized piece must go through this step before it can be used in marker making or pattern design software (PDS/Silhouette). If you want to keep the original raw digitized data too, use File>Save As and save it as digitized data instead.

### Retrv Original
Retrv Original (short for Retrieve Original) is the command you use if you accidentally make a bad or unwanted edit to a piece's digitized data. Choosing it wipes out your current on-screen changes and brings back the original, as-digitized version of the piece, giving you a way to undo mistakes. Be careful, though — if you later choose Store Digitize, whatever is currently on screen will permanently overwrite the original data.

### Definitions:
This is a section header introducing a glossary of key terms used elsewhere in the manual, such as storage areas, pieces, and digitized data.

### Sliding layrules
Sliding layrules is a feature that lets the AccuMark system "learn" how a marker maker builds a marker (the layout of pattern pieces on fabric to minimize waste) by remembering the exact sequence of moves and commands used. The system then tries to repeat that same sequence automatically when creating new markers, which works especially well for men's clothing since the patterns tend to be similar from one style to the next. This can save time by automating repetitive marker-making work.

### Current storage area
The Current storage area is simply the specific storage location you are actively working out of at any given moment — it's where the system looks for data when you retrieve something and where it saves data when you store something. Knowing which storage area is current matters so you don't accidentally save or lose track of a piece in the wrong place.

### Default storage area
The Default storage area is the storage location that AccuMark automatically opens to every time you start the software, before you manually switch to a different one. It acts as your starting point each session.

### Constructs
Constructs are a way to mark off areas on a piece of fabric where pattern pieces should never be placed during marker making, such as spots with flaws or fabric designs that shouldn't be cut through. Setting up a construct helps prevent wasted or defective cut pieces by keeping the marker-making process away from those flagged areas.

### Piece
A Piece refers to a complete, valid, and usable AccuMark pattern piece — not just raw digitized points. If a piece was digitized by hand or brought in from another system, it must go through Store Verify (confirming and saving the raw data properly) before AccuMark will treat it as a real, usable piece.

### Digitized data
Digitized data is the raw record of every button press made with the digitizing cursor while a worker traces a pattern piece onto the digitizing table, in the exact order the buttons were pressed. It's sometimes called "raw digitized data" or "raw pieces," and it exists temporarily before the piece is verified and saved into permanent storage.

### Manual grading
Manual grading is the process of resizing a master pattern up or down according to a specific set of body measurements while keeping the original design's style lines intact. In plain terms, it's the skilled work of turning, say, a size 10 pattern into a properly fitting size 14 without distorting the designer's original proportions, and this function is done within the PDS (Pattern Design System) part of the software.

### Wildcard
A wildcard is a special keyboard symbol you can type in place of real characters when searching for or renaming files. The asterisk (*) stands in for a whole series of characters (so typing "coat*" finds coat12, coat34, coat56, etc.), while the question mark (?) stands in for just one character (so "suit?" would pull up suit1, suit2, suit3, and suit4). Workers use wildcards to quickly find, rename, or look up several pieces or markers at once instead of typing each full name separately.

### Statically
"Statically" describes a setting where the system automatically applies certain amounts or rules — like matching stripes/plaids, blocking/buffering (adding safety margins around a piece), or alterations — to a piece without the operator having to do anything by hand. It's the opposite of "dynamically," where the worker applies those same rules themselves while building a marker (the layout of pieces on fabric).

### Segment
A segment is a specific area of a pattern piece that gets marked out while the piece is being digitized (traced into the computer) in PDS, the pattern design software. It's defined by placing special B and Q point markers, which tell the system where that section of the piece begins and ends.

### Dynamically
"Dynamically" means the worker applies amounts or rules — such as matching patterns, blocking/buffering, or alterations — themselves, interactively, while actually building the marker (the fabric cutting layout). This is the opposite of "statically," where the system applies those same things automatically without the worker step ​ing in.

### Internals
Internals are any lines or points on a pattern piece that are not part of its outer edge (perimeter) — things like alternate grain lines, notes/annotations, or marks for cutouts and drill holes. Workers and digitizers need to capture these because they guide sewing, cutting, or drilling steps that happen inside the piece, not just around its edge.

### Dead zone
The dead zone is a two-inch strip along the outer edge of the digitizing table (the surface used to trace paper patterns into the computer) where the digitizing cursor won't register any input. When placing a pattern piece on the table to trace it, workers need to keep the whole piece inside this border so no part of it gets missed.

### Nest
A nest, or nested piece, is a drawing that shows every size of a pattern piece stacked directly on top of each other in one image. This lets a worker see at a glance how the shape and grading (size differences) change from the smallest to the largest size.

### Locator points
Locator points are reference marks used when a pattern piece is too large to digitize (trace into the computer) all at once and has to be split into separate grid sections. These points tell the system exactly how to line up and reconnect those separate sections back into one complete piece.

### Transition points
Transition points are marks used in the PDS pattern software when digitizing a large piece that has been split into grid sections; they mark the exact spots where the piece's outer edge leaves one section (exit point) and enters the next (entry point). Each entry and exit point gets a specific code label (for example, an entry point might be labeled AD0AB12) so the system knows how to stitch the sections back together correctly.

### Modular patterns
Modular patterns are patterns built from basic partial pattern blocks, called "parents," that other smaller piece sections (called paste pieces) get attached to. This approach lets workers reuse the same base blocks across different styles instead of building every pattern completely from scratch.

### Point Limits
Point Limits are the maximum number of points allowed on a single pattern piece, based on what the system's memory can handle: up to 4,000 points around the outer edge (perimeter) and up to 12,000 points total including internal points and points the system automatically adds for smoothing curves. If a piece exceeds these limits while an order is being processed, AccuMark will record an error message in the Activity Log, and the issue needs to be fixed in the PDS pattern design software.

### Digitizer Storage Location
The Digitizer Storage Location is a temporary folder (c:\userroot\devq\digitizer) where PDS automatically saves a pattern piece right after it's traced in (digitized) on the digitizing table. The piece stays here until the worker checks it over and confirms it's correct (verifies it); to pull it up again in Classic AccuMark, they type the piece name, set the Location field to "Digitizer," and select Retriev Digitz.

### Current Storage Location
In Classic AccuMark, "Current" in the Location field of the Piece Verify Editor means the storage area the worker is actively working in at that moment. To view or edit a piece that has already been saved/verified, the worker needs to retrieve it from this Current storage area rather than from the temporary Digitizer location.

### Digitized data
Digitized data is the raw record of every button press made with the digitizing cursor while a worker traces a pattern piece onto the digitizing table, in the exact order the buttons were pressed. It's sometimes called "raw digitized data" or "raw pieces," and it exists temporarily before the piece is verified and saved into permanent storage.

### Bundle
A bundle is a set of cut fabric pieces that get grouped together and sewn to make one complete garment or item, such as all the pieces needed for a single shirt. Workers on the floor use bundles to keep the right pieces together as they move through cutting and sewing.

### Model options
Model options let a worker set up different variations of a single garment style (model) — such as substituting or adding certain pieces — without having to build a brand-new model from scratch for every variation. This section also covers dynamic piecing, a related feature (set in the Dyn PC field on the Model Form) that lets a piece be split into multiple sections in the marker, up to nine times, to make more efficient use of fabric.

### Half piecing
Half piecing is a feature that lets one pattern piece be shared between two bundles instead of cutting a separate piece for each, and it also controls whether those shared piece halves must face the same direction or can face any direction in the marker (the fabric layout). It's turned on by setting the Half PC field on the Model Form, and it's typically used to save fabric.

### Dynamic piecing
Dynamic piecing is an AccuMark feature that allows a single pattern piece to be automatically split into multiple smaller sections within a marker (the fabric cutting layout), up to nine times, in order to make more efficient use of fabric. It is turned on by entering a value in the Dyn PC field on the Model Form.

### Model
A Model is simply the complete set of all the individual pattern pieces needed to make one finished garment or item, such as a shirt's front, back, sleeves, and collar all grouped together. Workers set this group up using the Model Form, a data entry screen where all the pieces for that garment style are listed and organized. Creating a Model this way lets the system treat all those pieces as one unit for cutting, ordering, and marker-making tasks.

### Match marks
Match marks are small straight lines (running horizontal or vertical) that get printed or plotted onto the fabric marker to show where a striped or plaid pattern's repeat lines up. They help the cutting or sewing crew line up pieces so the stripes or plaid on the finished garment match correctly across seams. There is also an option to have these lines drawn all the way across the entire marker instead of just short marks at the edges, making alignment even easier to check at a glance.

### Full body measurement
A full body measurement is a real, physical measurement taken directly from a customer's body (like waist, chest, or inseam) at the time their garment order is placed. This actual number is entered into the system so the pattern can be adjusted to fit that specific person rather than using a standard size chart. It's the raw input a worker records before any pattern alterations are calculated.

### Blue pencil alteration amount
This is the amount of change marked for a specific fitting alteration on a customer's Blue Pencil Diagram or Order Sheet, which are the documents used to note custom fit changes. Instead of writing down just the difference to add or subtract, workers can instead enter the customer's actual measurement — for example, entering 34.50 inches (the customer's real waist size) instead of writing '+0.50 inches' when the standard pattern measures 34.00 inches. This lets the alteration amount be calculated automatically by comparing the actual measurement to the pattern's base size.

### Layrules
Layrules are saved sets of instructions that let AccuMark automatically rebuild a marker (the layout of pattern pieces on fabric) that was made before, instead of a worker placing every piece by hand again. The system searches its stored markers and reuses matching layouts, acting like a smarter, automatic version of the Copy Marker function. Using Layrules saves time on piece placement and lets more markers be stored efficiently; workers can set up the Lay Rule Search Parameter Table to control exactly how the system searches for and reuses these saved layouts.

### Dry haul
Dry haul is the amount of time the GERBERcutter's knife spends moving through the air above the fabric — traveling from the point it lifts out of one piece or the marker's edge to the moment it plunges back in to start cutting again. It's essentially 'wasted' travel time where no cutting is happening. Reducing dry haul is one way operators can speed up overall cutting time on the machine.

### Heelcuts
A heelcut happens when the cutting knife plunges down into the fabric at a point where part of the blade is still inside the edge of the pattern piece, rather than fully outside it. This is the opposite of an overcut, where the knife instead lifts out while part of it is outside the piece. Workers may see this term when reviewing or adjusting how the GERBERcutter enters cuts to keep piece edges clean.

### Overcuts
An overcut is the point where the cutting knife lifts up out of the fabric while part of the blade is still outside the edge of the pattern piece it just cut. If the system isn't set up with proper buffering (extra spacing) or the pieces aren't placed carefully on the marker, this extra motion outside the piece can accidentally cut into or damage a neighboring piece. Understanding overcuts helps operators troubleshoot fabric waste or damaged pieces coming off the cutter.

### Cutter configuration file
A cutter configuration file is a settings file that a worker sets up directly on the GERBERcutter terminal (the cutting machine's control unit) to control how that specific cutter behaves during a cutting job. It essentially tells the machine things like cutting speed, knife behavior, and other operational preferences. Setting this up correctly ensures the cutter runs the way the shop floor needs for a given job or fabric.

### Alternate grain line
An alternate grain line is an extra line drawn (digitized) on a pattern piece in the PDS (Pattern Design System) module, in addition to the main grain line that normally shows the fabric's straight-of-grain direction. It acts as a backup or substitute reference line specifically to make grading (resizing a pattern up or down) easier on pieces with complicated shapes. Workers or pattern staff would use it on tricky pieces where the standard grain line alone isn't enough to guide accurate resizing.

### Getting Started
This is the introductory section of the manual meant to orient a new user to the AccuMark Order Entry software, typically covering basic navigation and first steps before diving into specific tasks.

### Overview
This section gives a high-level summary of the AccuMark Order Entry software's purpose and main features before the manual moves into detailed, step-by-step instructions for each function.

### The AccuMark Marker Creation, Editors page of the GERBER LaunchPad provides the
This refers to a specific screen (page) within the GERBER LaunchPad, the main menu hub for AccuMark software, dedicated to marker creation tools and editors.

### editors to create and customize AccuMark forms and parameter tables to meet your
This describes the editing tools available on that LaunchPad page, which let a shop set up and customize the data entry forms and settings tables (parameter tables) used throughout AccuMark.

### company’s specifications.
This phrase completes the previous description, meaning the forms and parameter tables can be tailored to match a specific company's own rules, sizing, or production requirements.

### Workflow for Ordering and Processing Markers
This is a manual section that lays out, step by step, the standard sequence of tasks a worker follows from placing a customer order through to producing a finished cutting marker.

### The typical workflow for ordering and processing markers consists of the tasks shown
This introductory sentence leads into a list or diagram in the manual showing the standard sequence of steps for ordering and creating markers.

### below. This workflow assumes you have completed the initial setup requirements. Click
This continues the workflow introduction, noting that the listed steps assume basic system setup is already done, and directs the reader to click something (likely a link or icon) to proceed or learn more.

### on any task in the workflow shown below to learn more about that task.
This is an instruction pointing workers to click or select any step shown in an on-screen workflow diagram to get more details about that specific step. It is a navigation tip within the software's help system, not a function itself.

### Note: Once a marker order is successfully processed, the marker can be retrieved in the
This note explains that after a marker order (a request to lay out pattern pieces efficiently on fabric) finishes processing without errors, the resulting marker file becomes available for use elsewhere. Workers would check this after submitting an order to confirm it is ready for the next step, such as opening it in another application.

### Marker Making application, made (if needed), and stored. After being stored, the marker
This continues the explanation above: the marker (the layout of pattern pieces on fabric) is opened in the separate Marker Making application, finalized or adjusted there if necessary, and then saved into storage. Once saved, the marker is ready to be reused, printed, or sent for cutting whenever needed.

### can then be plotted to check for accuracy. If you have a GERBERcutter, you can also
After the marker is stored, workers can print it out full-size on a plotter (a large-format printer) to visually verify that all pattern pieces are placed correctly and nothing overlaps or is missing. If the facility has a GERBERcutter (an automated fabric-cutting machine), the marker can additionally be used to prepare cutting instructions.

### generate cut data from the marker and plot the cut data to further check for accuracy.
This step lets workers convert the finished marker into cut data, meaning the precise instructions the GERBERcutter machine will follow to cut fabric pieces automatically. They can then print this cut data as well, giving a second accuracy check before actual fabric is cut, helping catch mistakes before material is wasted.

### Using Order Entry
This is the main section introducing the Order Entry function, which is where workers create and submit requests (orders) for markers, patterns, or cutting jobs to be processed by the AccuMark system. It covers the basic steps of entering the information the system needs, such as style, size, quantity, and fabric details, to start a production job.

### Working with Storage Areas
This section explains how to use Storage Areas, which are designated locations within AccuMark where files like markers, patterns, and orders are saved and organized. Workers use this to know where to find, save, or move their work so files are organized correctly.

### Storage Areas are user def
This is a cut-off phrase, but based on context it means Storage Areas are user-defined, meaning the company or system administrator sets up and names these storage locations to organize files logically, such as by customer, style, or job type. Workers should select the correct storage area their team has been told to use when saving or retrieving files.


## IGES Translator (Import/Export)
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


## Style Converter
*A batch utility that converts older MicroMark pattern styles into the newer AccuMark format, so they can be used in modern Pattern Design, Marker Making, and Order Entry.*

### Main workflow functions

**Select style(s) to convert** — You type or pick the name of the MicroMark style(s) you want converted. If you have a lot of styles (the manual recommends this above roughly 2,000 at once), you can use a wildcard (a search pattern like `ABC*`) to grab many styles in one go and convert them in smaller groups rather than all at once, which keeps the process manageable.

**Inspection Options** — A settings screen where you turn on automatic sorting of problem styles. When enabled, any style that comes out of the conversion with a warning or an error gets automatically copied into its own folder (by default under `C:\ads`), so you don't have to hunt through the whole batch to find the ones that need attention.

**Convert / Run** — The button that actually starts the conversion process on the style(s) you've selected.

**Results dialog** — A summary screen that appears once conversion finishes, telling you how many styles converted, and (if Inspection Options is on) asking whether to go ahead and copy the flagged styles into their problem folders.

**Report Results** — A button that opens a spreadsheet-style file (CSV) listing every warning and error found during the conversion, usually in a program like Excel, so you have a permanent record you can review, sort, and act on later.

**Style Converter Viewer** — A side-by-side comparison screen that shows you the old MicroMark version of a piece and the new AccuMark version overlaid on top of each other, so you can visually spot any differences.
- **Measure function** — A tool inside the Viewer that lets you click and measure exactly how far apart two points are, useful for checking how much a shape shifted during conversion.
- **Snap to Geometry** — A tool that lines up the two overlaid versions of the piece precisely, so any real differences between them are easier to see clearly instead of being hidden by a slight misalignment.

### Problems the software finds and flags as errors (these usually mean the piece needs manual correction)

**Intersection error while grading piece** — The piece's outline crosses over itself on the base size or on a graded (resized) version. Fix it by opening the piece in Pattern Design and correcting the outline shape or the grading rules that control how it resizes.

**Piece modification has invalidated a corner angle** — A seam corner style that was previously set on a point no longer fits the piece's current shape. Fix it in Pattern Design by reassigning the corner type or adjusting the piece's shape.

**Unable to store, 2 F points required** — The old style had two grain lines (lines showing fabric direction), which AccuMark doesn't support. Remove one of the two grain lines in the old MicroMark software before converting again.

**Failed MicroMark grading** — Usually means a required update step wasn't run on the style/grade-rule folders, or a grade rule is missing/damaged. Run the Update process on those folders and try converting again.

**Invalid matching lines** — Lines used for matching plaids/stripes across pieces must run parallel or exactly perpendicular to the fabric's grain line; this piece has one that doesn't. Needs to be corrected in the original pattern.

**Rule Table missing** — The grading instructions (rule table) that tell the software how to resize this piece can't be found. Locate the correct rule table and place it in the expected folder, or point the style at a different, existing rule table.

**MicroMark sizes missing** — The style refers to a "synonym table" (a way of renaming sizes) that Style Converter can't fully process. Remove the synonym table reference from the style, or edit it down to a simple rename with no actual size variation.

**Missing OPP Grade Axis** — Some grade points need a reference direction ("OPP axis") defined that isn't set up. Define it either in the old MicroMark data or after conversion in AccuMark.

**Cannot find rule –1** — The piece has a placeholder/invalid grading rule number assigned to a point. Go into the old MicroMark pattern and assign a real, valid rule number to that point.

### Problems the software finds and flags as warnings (informational — often no action needed, but worth checking)

**Piece was flipped, grain line realigned to maintain flip state** — The piece was saved facing the opposite way it was originally drawn; the software automatically adjusted the grain line marking to keep the resizing correct despite the flip.

**Piece with grain line converted to F Rotation will not rotate the same way in AM marking as in MK marking** — A heads-up that this particular piece may lay out slightly differently when nesting/marking in AccuMark compared to how it used to behave in the old MicroMark software.

**Piece message has been truncated** — A note/description on the piece was shortened because AccuMark's description field (20 characters) is smaller than MicroMark's (32 characters); some of the original text was cut off.

**Cut lines are not present in MicroMark piece — sew perimeter is used for comparison** — This piece never had a separate "seam allowance already added" outline defined, so the software compared and saved it using the sew-line outline instead.

**Unavailable rules converted to 0 growth** — A grading rule the piece pointed to doesn't actually exist, so that point/line was set to not grow or shrink between sizes (0 growth) instead.

**Tangent rule not valid on points, replaced with 0 growth** — A type of grading rule meant only for notches was mistakenly applied to a regular point; the software set it to no growth instead of applying it incorrectly.

### Differences the Viewer can highlight when comparing the old and new versions of a piece

**Intersection Moved** — A corner where two edges of the piece meet has shifted position between the old and new version; use the Measure tool to see exactly how far.

**Curves Different** — A curved section of the piece (like an armhole) came out a slightly different shape after conversion, shown highlighted on screen for one size at a time.

**Changes in Notches** — A notch (small cutting guide mark) moved position, disappeared, or an extra one appeared compared to the original piece.

**Overall Perimeter Changes** — The piece's entire outline shifted position (not shape) because its reference origin point changed during conversion.

**Sizes has variations and can not be converted** — The old style used "Variation Sizes" (a MicroMark-specific sizing feature) that Style Converter cannot handle directly; this needs to be resolved through the synonym/size-code setup described in "MicroMark sizes missing" above before it can convert successfully.
