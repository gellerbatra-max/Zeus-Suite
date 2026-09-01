# Function Definitions — ## Order Entry (AccuMark Professional Edition)
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
