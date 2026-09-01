# Complete Function Reference — Legacy Gerber Applications
*Every menu item, command, dialog field, and command-line switch documented in the manuals for
the five applications used throughout this analysis (Pattern Design, Marker Making, Order Entry,
IGES Translator, Style Converter).*

**Source and method:** Pattern Design, Marker Making, and Order Entry lists are extracted
directly from each manual's own Table of Contents, which in AccuMark/PDS2000 documentation
enumerates every menu, sub-menu, dialog, and named function — this is the exhaustive index the
manual itself ships with, not a curated subset. Indentation below follows the source TOC's own
chapter/sub-item structure (chapters as `###` headers, functions as bullets); a small number of
items may be mis-leveled where the original PDF's typographic cues (dot-leaders) were ambiguous
in text extraction — the item names themselves are verbatim from the manual. IGES and Style
Converter have no formal TOC (they are short, task-focused manuals) — their sections below are
built from the full body text: IGES's command-line switches and the IGES.INI parameter file
options for the former, and every documented button/dialog/error/warning/mismatch condition for
the latter.

**Scale, for context:** Pattern Design's manual alone indexes 552 functions/sections — the
underlying AccuMark/PDS2000 pattern-design environment is by far the largest of the five in
scope. Marker Making indexes 200 and Order Entry 422 (Order Entry's manual bundles
digitizing, grading, and AutoMark functions alongside order/marker management, which is why its
count is large). IGES and Style Converter are deliberately short, single-purpose utilities.

---

## Pattern Design (PDS 2000 / Silhouette 2000)
*552 documented functions/sections*

### Getting Started
### Glossary of Terms
### Pattern Design Work Space
- Get Acquainted with the Work Space
- Menu Bar
- Tool Bar
- Using the AccuMark Menu
- Using the MicroMark Menu
- MicroMark Function Keys
- MicroMark Tool Bar
- Piece/Icon Menu
- Working with Piece/Icon Menu
- User Input Box
- Status Bar
- Info Bar
- Prompt Bar
- Quick Open
- Rulers
### Set Up Your System
- Customizing Pattern Design Work Space
- Open, Close, and Arrange Work Areas
- Display Pieces in the Work Area
- Docking Tool Bars, Menus, and User Input Box
- Use Preferences/Options
- Preferences/Options
- Setting Draft Preferences/Options
- General Page
- Setting General Preferences/Options
- Changing Preferences/Options for Piece Display
- Changing Preferences/Options for Piece Selection and Tracking
### Changing Preferences/Options for AccuMark or MicroMark Environment
- Changing Preferences/Options for Work Space and Misc.
- Options Input Section
- User Input Command/Prompt Section
- User Input Controls Section
- Value Input Section
- Color Page
- Setting Color Preferences/Options
- Changing Piece Colors
- Changing Nest Colors
- Changing Text and Miscellaneous Colors
- Plotter Page
- Setting Plotter Preferences/Options
- Changing Plotter Defaults
- Changing Cut Parameter Overrides
- Style Page
- Setting Style Preferences/Options
- Changing Preferences/Options for Naming Styles
- Changing Preferences/Options for Exporting Grain Line
- Changing Style Preferences/Options for Notches
- Paths Page
- Setting Paths Preferences/Options
- Changing Paths for Storage Areas
- Changing Paths for Styles
- Changing Paths for Import Files
- Use Screen Layout
- Overview of Customizing with Screen Layout
- Screen Layout
- Display Guidelines
- Snap to Grid, Geometry, or Precision
- Keyboard
- Use Custom Toolbars
- Custom Toolbars
- Add or Delete Tool Bar and Buttons
- For the Piece/Icon Menu
- Displaying the Piece/Icon Menu
- Deleting Pieces from the Piece/Icon Menu
- Placing Pieces into the Work Area
- Piece Information from the Piece/Icon Menu
- For AccuMark or MicroMark
- Setup for AccuMark or MicroMark Grading/Marking System
- Set Preferences for Environment and Paths
- Customize Work Space for AccuMark
- Customize Work Space for MicroMark
- Mark Request and Orderload Differences
- Differences
### Differences Between PDS 2000/Silhouette 2000 and AccuMark or MicroMark
- Selection, Options and Tracking Differences
- Access Features Formerly in AccuMark Popup Menu
- Accessing Features Formerly in MicroMark Function Keys
### Learn the Basics
- Overview of Working in PDS 2000/Silhouette 2000
- Piece Geometry
- Geometry Colors
- Cursor Shape Changes
- Moving Pieces in Work Area
- Arranging Multiple Work Areas
- Quick Keys
- Short Cuts
- Function Keys
- Hot Keys
- Keyboard Keys
- Using Zoom Commands
- Select and Move Points, Lines, and Pieces
- Selecting Multiple Points, Lines, or Pieces
- Selecting a Range with Thumbtacks
- Ending Selection to Continue
- Selecting Points/Locations on Multiple Lines/Pieces
- Select and Move Points, Lines, and Pieces
- Work in Cursor and Value Modes
- Getting Acquainted with User Input Box
- Changing between Input Modes
- Work in Value/Cursor Mode
- Working in Cursor Mode
- Working in Value Mode
- Options Pop-up Menus
- Options Pop-up Menu
- Using Options Pop-up Menus for Commands
- Options for Making Selections in Commands
- Options for Point Location
- Options for Lines
- Using Options Pop-up Menu for Work Area Tasks
### File Management
- Overview of File Menu
- File Structures and Data Equivalents Differences
- New
- Open
- Create/Edit Model
- Close
- Close Style/Model
- Style Description
- Style/Piece Manager
- Model and Style Description Differences
- Import
- Recent File
- Printing, Plotting, and Cutting
- Exit
- Using Style Description
- Setting Sample Size for Style Description
- Setting Style Information for Style Description
- Setting Marker Preparation and Shrinkage for Style Description
- Using the Style Description Page
- Using the Piece Description Page
- Adding or Deleting Pieces and Descriptions
- Using the Cutter's Must Page
- Checking Style History
- Save Pieces, Models, or Styles
- Setting Piece Blocking for Style Description
- Setting Piece Information for Style Description
- Setting Piece Restrictions for Style Description
- Saving Pieces, Models, or Styles
- Saving and Converting Data
- Save - Current Model, Style, or Pieces
- Prefix Names
- Save As
- Printing
- Print
- Printing
- Print Preview
- Print Setup
- Plotting/Cutting
- Plot
- Plotting
- Plot Preview
- Plot Setup
- Plot Text
- Submit Sample Request
### Make Edits
- Overview of the Edit Menu
- Undo
- Redo
- Set Selected
- Add Pieces
- Current Pieces
- Remove Pieces
- Select All
- Clear All
- Delete Pieces from Work Area
- Edit Point, Line, and Piece Info
- Edit Point Info
- Showing Point Info
- Edit Line Info
- Edit Piece Info
- Setting Up for Tracking
- Use Tracking to Edit
### Change View Options
- Overview of View Menu
- Piece - Seam Amounts
- Refresh Display
- Use Zoom Commands
- Zoom In
- Zoom Out
- Zoom - Full Scale
- Zoom to Selected
- Zoom - 1 : 1
- Zoom - Separate Pieces
- Verify Points
- Point - All Points
- Point - Intermediate Points
- Point - Point Numbers
- Point - Grade Rules
- Point - Notch Points
- Point - Point Types/Attributes
- Point Types and Modifiers
- Attributes
- Point - Total Piece Points
- View Lines
- Line - Numbers
- Line - Names
- Line - Types/Labels
- Line Modifiers - Types and Labels
- Line - Verify by Label
- Line - Seam Corner Types
- Hide/Ignore Lines
- Line - Hide/Ignore Perimeter
- Line - Hide/Ignore Internal
- Line - Hide/Ignore Reset
- Show Grading
- Grade - Show Base Size
- Grade - Show All Sizes
- Grade - Show Breaks
- Grade - Show Selected Sizes
- Grade - Show Non-base Size
- Grade - Stack On/Off
- Grade - F Rotation
- Clear Nest
### Work with Points
- Overview of Point Menu
- Add Point
- Adding Multiple Points
- Mark X Point
- Modifying Points
- Point Intersect
- Delete Point
- Reduce Points
- Total Piece Points
- Copy Point Num
- Add Notches
- Working with Notches
- Add Notch
- Intersection Notch
- Add Multiple Drills and Points
- Add Multiple - Add Drills
- Add Multiple - Add Drills Dist
- Add Multiple - Add Points Line
- Add Multiple - Add Points Ln Dist
- Modify Points
- Modify Points - Angled Notch
- Modify Points - Align 2 Points
- Moving Points
- Modify Points - Move Point
- Modify Points - Move Pt Line/Slide
- Modify Points - Move Point Horiz
- Modify Points - Move Point Vert
- Modify Points - Move Smooth
- Modify Points - Move Smooth Line
- Modify Points - Move Smooth Horiz
- Modify Points - Move Smooth Vert
- Verifying Points
### Work with Lines
- Overview of Line Menu
- Delete Line
- Replace Line
- Swap Line
- Unclipped Perimeter
- Clipped Perimeter
- Perimeter Clipped/Unclipped Sample
- Create Lines
- Overview of Create Line Menu
- Create Line - Digitized
- Create Line - Curved
- Create Line - 2 Point
- Create Line - Offset Even
- Create Line - Offset Uneven
- Create Line - Copy Line
- Create Line - Mirror
- Create Line - Create Blend
- Hide/Ignore Lines
- Moving Lines
- Internal Line Labels
- Tangent Lines
- Create Line - Tangent On Line
- Create Line - Tangent Off Line
- Create Line - Tangent 2 Circ
- Creating Tangent Lines
- Perpendicular Lines
- Perp Line - Perp On Line
- Perp Line - Perp Off Line
- Perp Line - Perp 2 Points
- Creating Perpendicular Lines
- Conics
- Conics - Circle Ctr Rad
- Conics - Circle Ctr Cirm
- Conics - Circle 2 Pt Center
- Conics - Circle 3 Pt
- Conics - Circle Tang 1 Line
- Conics - Circle Tang 2 Line
- Conics - Curved Intersection
- Conics - Oval Orient
- Conics - Oval Focus
- Creating Circles and Ovals
- Modify Lines
- Modify Line - Move Offset
- Modify Line - Move Line
- Modify Line - Move Line Anchor
- Modify Line - Move Range
- Modify Line - Make Move Parallel
- Modify Line - Make Parallel
- Modify Line - Rotate Line
- Modify Line - Move and Rotate
- Modify Line - Set and Rotate
- Modify Line - Reshape Line
- Modify Line - Adjust Length
- Modify Line - Smooth
- Modify Line - Merge
- Modify Line - Split
- Modify Line - Clip
- Modify Line - Open Line
- Modify Line - Flatten Line Segment
- Modify Line - Edit Line Names
- Modify Line - Copy Line Names
- Overview of Modify Line Menu
### Work with Pieces
- Overview of Piece Menu
- About Pieces
- Differences in Working with Pieces
- Fold Keep
- Delete Piece from Work Area
- Combine/Merge
- Shrink/Stretch
- Annotate Piece
- Hide Annotations
- Piece to Menu
- Showing Grading for Pieces
- Create Pieces
- Creating Pieces
- Create Piece - Rectangle
- Create Piece - Circle
- Create Piece - Skirt
- Create Piece - Oval
- Create Piece - Collar
- Create Piece - Facing
- Create Piece - Copy
- -Create Piece - Extract Piece
- Trace Pieces
- Create Piece - Trace Normal - Sew
- Create Piece - Trace Normal - Cut
- Create Piece - Trace Mirrored - Sew
- Create Piece - Trace Mirrored - Cut
- Create Piece - Trace Scored - Sew
- Create Piece - Trace Scored - Cut
- Tracing to Create Pieces
- Seams and Corners
- Overview of Working with Corners
- Overview of Working with Seams
- Viewing Seams and Amounts
- About Seam Differences
- Seam - Define/Add Seam
- Seam - Hide/Remove Seam
- Seam - Sever Corner
- Seam - Swap Sew/Cut
- Seam - Update Seam
- Seam - Copy Piece No Seam
- Seam - Fix Bound Type
- Seam - Sever Boundary
- Seam - Relate Boundary
- Seam - Reset SA Values
- Corners
- Notch Options for Corners
- Seam - Corners On/Off
- Seam - Remove Corner
- Seam - Regular Corner
- Seam - Slant Corner
- Seam - Mitered Corner
- Seam - Double Miter Corner
- Seam - Tab Corner
- Seam - Nub Extension Corner
- Seam - Mirrored Corner
- Seam - Turnback Corner
- Seam - Frame Corner
- Seam - Perpendicular Step Corner
- Seam - Bisect Step Corner
- Seam - Squared Corner
- Seam - Match Corners
- Modify Pieces
- Modify Piece - Move Piece
- Modify Piece - Flip Piece
- Modify Piece - Rotate Piece
- Modify Piece - Set and Rotate/Lock
- Modify Piece - Walk Pieces
- Modify Piece - Use Position
- Modify Piece - Define Position
- Modify Piece - Remove Position
- Modify Piece - Realign Grain/Grade Ref
- Modify Piece - Lock to Grid
- Modify Piece - Anchor/Unanchor
- Modifying Pieces
- Split Pieces
- Split on Line
- Split on Digitized Line
- Split Point to Point
- Split Horizontal
- Split Vertical
- Split Diagonal Left
- Split Diagonal Right
- Creating Pieces using Split Lines
- Mirrored Pieces
- Working with a Mirrored Piece
- Mirror Piece
- Fold Mirror
- Unfold Mirror
- Open Mirror
### Pleats
- Working with Pleats
- Pleats - Knife Pleat
- Pleats - Box Pleat
- Pleats - Variable Pleat
- Pleats - Taper Pleat
- Adding Pleats to Pieces
### Darts
- Working with Darts
- Creating and Working with Darts
- Darts - Rotate
- Darts - Distribute Same Line
- Darts - Distribute/Rotate
- Darts - Combine Same Line
- Darts - Combine Diff Line
- Darts - Add Dart
- Darts - Add Dart With Fullness
- Darts - Change Dart Tip
- Darts - Equal Dart Legs
- Darts - Balanced Resize
- Darts - One Sided Resize
- Darts - Open Dart
- Darts - Fold/Close Dart End
- Darts - Smooth Line
- Darts - Flatten Line Segment
### Fullness
- Fullness - Fullness
- Adding Fullness to Pieces
- Fullness - 1 Point Fullness
- Fullness - Variable Fullness
- Fullness - Tapered Fullness
- Fullness - Parallel Fullness
- Fullness - Taper Slash n Spread (Expert Edition Only)
- Fullness - Parallel Slash n Spread (Expert Edition Only)
### Asymmetrical Folds
- Working with Asymmetrical Folds
- Asymm Fold - Line Fold
- Asymm Fold - Line to Line Fold
- Asymm Fold - Match Points
- Assym Fold - Dart Fold
- Asymm Fold - Pleat Fold
- Asymm Fold - Perim Pt Fold
- Asymm Fold - Unfold
- Asymm Fold - Unfold Keep
### Grade Rules
- Overview of Grade Menu
- Creating or Editing Grade Rules
- Hints on Viewing and Working with Grading
- Copy Size Line
- Make Base Size
- Add Size Break
- Assign Rule Table
- Modifying Grade Rules
- Create Nest
- Clear Charts
- Measure Line
- Working with Line Size Charts
- Export Rules
- Create/Edit Grade Rules
- Create/Edit Rules – Edit Delta
- Create/Edit Rules – Create Delta
- Create/Edit Rules – Edit Offset
- Create/Edit Rules – Create Offset
- Working with Create/Edit Forms
- Working with Distances Grade Forms
- Create/Edit Rules – Match Line X
- Create/Edit Rules – Match Line Y
- Create/Edit Rules – Keep Angle Apex
- Create/Edit Rules – Keep Angle Edge X
- Create/Edit Rules – Keep Angle Edge Y
- Create/Edit Rules – Keep Angle Edge Ext
- Create/Edit Rules – Parallel X
- Create/Edit Rules – Parallel Y
- Create/Edit Rules – Parallel Ext
- Create/Edit Rules – Specify Distance
- Create/Edit Rules – Intersection X
- Create/Edit Rules – Intersection Y
- Create/Edit Rules – Intersect Parallel
- Create/Edit Rules - Intersection Offset
- Modify Grade Rules
- Modify Rule – Change Grd Rule
- Modify Rule – Add Grade Point
- Modify Rule - Copy Table Rule
- Modify Rule - Copy Grade Rule
- Modify Rule – Copy X Rule
- Modify Rule – Copy Y Rule
- Modify Rule – Copy Nest Rule
- Modify Rule – Copy Nest X
- Modify Rule – Copy Nest Y
- Modify Rule – Flip X Rule
- Modify Rule – Flip Y Rule
- Modify Rule – Rotate 90
- MicroMark Grading Types
- Working with MicroMark Grading
- Tangent Grading
- Perpendicular Grading
- Opposite Grading
- Blend Grading
- Proportional Grading
- Paste Grading
- Line Grading
- Variation Grading
### Measure Menu
- Overview of Measure Menu
- Line Length
- Distance 2 Line
- Perimeter 2 Pt/ Measure Along Piece
- Distance 2 Pt/ Measure Straight
- Piece Perimeter
- Piece Area
- Angle
- Clear Measurements
### Draft/Sketch
- Sketch
- Line - Curve
- Note - Illustrate
- Note Pen Resolution
- Point Filter
- Reorient
- Draft Scale
- Create Piece
- Draft Trace
- Trim/Extend Line
- Trim/Extend Piece
- Stream Sketch
- Sketch Pen Resolution
- Basics of Drafting Pieces in Silhouette 2000
- Create Draft Pieces and Save Working Pieces
- Working with Silhouette Table, Screen, and Pen
- Using the Pen
- Using the Eraser
- Hints on Setting Preferences/Options
- Drafting on the Silhouette Table
- Basics of Drafting Pieces in Silhouette 2000
- Practical Application Examples
- Draft a Design
- Design From Sloper
- Create and Modify a First Pattern
- Copy an Assembled Garment
- Alter Patterns
- Add Designs to Patterns
- Armhole/Sleeve Cap - Practical Exercise
- Practical Silhouette 2000 Applications
### Expert Edition
- Expert Edition
- Armhole/Sleevecap (Expert Edition Only)
- Measure Specs (Expert Edition Only)
- Create Binding (Expert Edition Only)
- Grading of Binding (Expert Edition Only)
- Multiple Slash and Spread (Expert Edition Only)

## Marker Making (AccuMark Professional Edition)
*200 documented functions/sections*

### Getting Started
- Settings/Marker Display
- Help
### Marker Making
- The Marker Making Workplace
- Work Area
### Main Menu
- File Menu
- Edit Menu
- View Menu
- Piece Menu
- Bundle Menu
- Marker Menu
- Layrule Menu
- Tools Menu
### Menu Functions
- Settings
### Right Mouse Toolbox
- Toolbox
- Toolbox Functions
- Toolbox Modifiers
### Add a Piece
### Add a Bundle
### Delete Piece
### Delete Bundle
### Create Block
### Creating a Rectangular Fuse Block
### Manually Creating Fused Blocks
### Modify Block Fuse
### Copy Fuse Block
### Delete Fuse Block
### Delete All Fused Blocks
### Create Fusing Marker
### Workflow for Block Fusing When Using a GERBERcutter
### Bundle/Unplace
### Bundle/Select
### Bundle/Flip
### Bundle/Reset Orientation
### Storage Areas
### File/Open
### File/Open Next Unmade
### File/Open Next Made
### File/Open Next
### File/Open Original
### File/Open Previous
### File/Save
### File/Save Temporary
### Look in
### Up One Level
### Create New Storage Area
### List View
### Details View
### File Name
### File Filter
### Save As
### MSDE for AccuMark Storage Areas
### Dynamic Split/Join
### Dynamic Split/Manual
### Dynamic Split/Left
### Dynamic Split/Right
### Dynamic Split/Top
### Dynamic Split/Bottom
### Layrules menu in MedPro
### Layrules/Positional/Search
### Layrules/Positional/Apply
### Layrules/Positional/Save Named
### Layrules/Positional/Save Searched
### Layrules/Sliding/Create
### Layrules/Sliding/Modify
### Layrules/Sliding/Search
### Layrules/Sliding/Apply
### Full Length
### Marker/Split
### Marker/Copy
### Marker/Attach
### Marker/Flip on X Axis
### Marker/Flip/on Y Axis
### Marker/Flip/XY Axis
### Vertical Line
### Horizontal Line
### Manual Line
### Delete Line
### Annotate Line
### Splice/Automatic
### Delete /Splice
### Bump Lines
### Marry/Create
### Marry/Modify
### Marry/Delete
### Marry/Delete All
### Measure/Point to Point
### Measure/Piece to Piece
### Measure/Piece to Edge
### Return
### Marry
### Conditions of Marriages
### Block Fuse
### Scoop
### Dynamic Alter
### Dynamic Split
### Measure
### Sliding Layrules
### Shrink and Stretch
### Icon Toolbar
### Configurable Toolbar
### Scoop Create
### Scoop Modify
### Scoop Delete
### Scoop Apply
### Scoop Build Up
### Scoop Build Right
### Scoop Build Down
### Scoop Build Left
### Unplace All
### Unplace Small
### Block
### Buffer
### Return All
### Return Unplaced
### Return Bundle
### Working with the Toolbox
### Auto Slide
### Area
### Length
### Height
### X Alter
### Y Alter
### XY Alter
### Group Slide
### Butt
### Overlap
### Align
### Flip
### Rotate
### 45 CW
### 45 CCW
### 90 CW
### 90 CCW
### 180 ROT
### Tilt CW
### Tilt CCW
### Variable
### Place
### Block/Buffer
### Split
### Fold
### Center
### Matching
### Free Rotate
### Global  Override
### Toolbox Override
### Placed
### Unplaced
### Icons
### Fit Piece
### Float Piece
### Step Piece
### Numeric Keypad Functions
### Reset Tilt
### Center
### Step
### Float
### Tubular Fold/Piece Count Adjustment
### Getting Started
### Using Marker Making
### Using the Mouse & the Stylus
### Icon Menu
### Marker Info
### Scroll Bar
### Message Line
### Placing Pieces in the Marker
### Placing Matched Pieces into a Marker
### Choosing Menu Commands
### Exit
### Storage Areas & Drives
### Dialog Boxes
### Lookups
### Layrules
### Marquee Selection Box
### Changing Settings
### Big Scale
### Zoom
### Refresh Display
### Creating Sliding Layrules
### Marry
### Marker Area Scaling
### Maximum Data Items Allowed
### Maximum Marker Length
### Block or Buffer Split Pieces
### Prompt Bar
### Piece count, automatic update
### Welcome to the AccuMark Professional Edition
### Settings/Piece Display
### Validate for InVision/AccuMatch
### Settings/Matching
### Settings/Global
### Settings/Splice
### Settings/Block Fuse
### Import
### Index

## Order Entry (AccuMark Professional Edition)
*422 documented functions/sections*

### Getting Started
- Overview
- Workflow for Ordering and Processing Markers
### Using Order Entry
- Working with Storage Areas
### Activity Log
### Alteration Form
### Annotation Form
- Annotation Format
### Block Buffer Form
### Cut Generation Form
### Cut Generation Parameter Table Form
### Cut Plot Form
### GERBER LaunchPad
- Pattern Processing, Digitizing, PDS
- Marker Creation, Editors
- Plotting and Cutting
- AccuMark Explorer, Utilities
- Documentation
### Lay Limits Form
### Layrule Search Parameter Table Form
### Marker Plot Form
- Processing Marker Orders
### Marker Plot Parameter Table
### Matching Form
### Model Form
- Model Options Editor
### Notch Form
### Order Form
- To order a marker
### Order Process
- Process Order
### Size Code Form
### User Environment
### Verify
### Generating Cut Data
### Preparing the Pieces You Want to Cut
### Assigning Cutter Internals
### Cutting Drill Hole Symbols
### To complete a Cutter Parameter Table
### To process marker data into cut data
### Plotting Cut Data to Verify Accuracy
### To plot a marker cut file
### To create an exported cut data file
### Exporting Cut Data
### Setting Up a Notch Parameter Table for Cutting
### Setting Up a Blocking/Buffering Rule Table for Cutting
### Setting Up a Lay Limits Table for Cutting
### Export File
### Label Tool Mapping
### Applying Cutter Point Attributes
### Configuration Dialog Box
### Working with Layrules
### Positional Layrules
### Layrule Features
### Sliding Layrules
### To create a sliding layrule
### Advantages of Using Layrules
### Considerations for Using Positional Layrules
### Naming Layrules
### Naming Positional Layrules Using Save Name
### Naming Positional Layrules Using Search Criteria
### Set Up for Using Positional Layrules
### To order a marker with layrules
### Setting Up Matching Requirements
### Point Matching Versus Line Matching
### Using Points and Rules to Set Up Matching
### Using Lines and Labels to Set Up Matching
### Standard Matching Versus 5-Star Matching
### Choosing a Matching Method on the Order Form
### Choosing a Matching Method in Marker Making
### Standard Matching
### 5-Star Matching
### Entering Multiple Offsets on the Order Form
### Entering/Changing Repeat and Offset Values in Marker Making100
### To create a matching rules table for  piece-to-piece, or piece-to-fabric
### matching
### Piece-To-Fabric Matching Chart
### To order a marker with matching
### Changing Matching Information in Marker Making
### Grouping Pieces to Create Models
### To create a model
### To set up model options
### To retrieve and edit a model
### To display an existing model option
### To copy a model option
### To add a model option
### To delete a model option
### Defining Paste Pieces in Model Options
### Model Editor
### To shutdown Order Entry
### To customize the Order Entry toolbar
### To edit a User Environment Parameter Table
### To create a new User Environment Parameter Table
### To use a different User Environment Parameter Table
### To edit a Notch Parameter Table
### To create a Notch Parameter Table
### To View the Activity Log
### To clear all items from the Activity Log
### Setting Up Annotation Requirements
### To create an annotation library
### To retrieve and edit an annotation library
### Setting Up Lay Limit Requirements
### To create a lay limits table
### To retrieve and edit a lay limits table
### Setting Up Blocking/Buffering Requirements
### To create a blocking/buffering rule table
### To retrieve and edit a blocking/buffering rule table
### Static versus Dynamic Blocking/Buffering
### Applying Blocking/Buffering
### To Change the grade rule values in a specific column
### To Clear the grade rule values in a specific column
### Pattern Conversion Wizard
### Marker Creation, Editors Page
### Toolbar
### Model
### Model Options
### Annotation
### Lay Limits
### Alteration
### Size Code
### Block Buffer
### Matching
### Multi Order
### User Environment
### Layrule Search
### Notch
### Piece Plot Parameter Table Field Explanations
### Marker Plot
### Cut Generation Parameter Table
### Process
### Activity log
### Clear All
### Cut data
### ASCII
### Category
### Fields
### Next Page
### Previous Page
### Print Plot
### View Plot
### Page Up
### Page Down
### Fabric type codes
### Cutdown master
### GERBERlabeller
### Go To Top
### Go To Bottom
### Delete All Job
### Delete Jobs
### Plot Now
### Stop Immediate
### Print
### Process Group
### Stop After
### Restart Queue
### APSM
### Next Model
### Previous Model
### Go To Model
### Copy Model
### Add Model
### Delete Model
### Bite length
### Group
### Delete All
### Delete
### Delete Active
### Restart Active
### Clear Owner
### New Page
### Set Media
### Library
### Blocking
### Buffering
### Add Rule
### Delete Rule
### Next Rule
### Previous Rule
### Hold points
### Move points
### Go To Act Size
### Go To Ord Size
### Alteration base amount
### Layrule Proc
### Load Multi-List
### Copy
### Paste
### Drill symbols
### Positional layrules
### Force Layrule
### Lr-Search-Tbl
### Copy Marker
### Annotate an Attached Marker
### Decimal Notation
### Import and Export User Settings
### Storage Areas
### Notch Types
### Shortcuts
### Quick Keys
### Hot Links
### Field Types
### Sticky Fields
### Rotary Fields
### Text Fields
### Lookup Fields
### To display and use a Lookup Field
### Networking
### Printing
### Network Plotting
### Fatal Error Report
### View System Information
### Version Info
### Maximum Data Items Allowed
### Maximum Marker Length
### Checking Pieces for Accuracy
### Hardware Configuration
### MSDE for AccuMark Storage Areas
### Print a Hard Copy of the User's Guide
- Print a Hard Copy of the User's Guide
### Ordering Markers
### Setting Up Halfpiece Sharing
### Nested Halfpieces
### To set up a model with halfpiece sharing
### To order a marker with halfpiece sharing
### Setting up Cutdowns
### To order a marker with cutdowns
### To order a marker with constructs
### To order a marker for block fusing
### To order a marker from an existing marker
### To order a marker for fabric that shrinks or stretches
### Order Options
### To process a marker order
### To verify the status of a processed order
### To process a marker using layrules
### To process a marker using load multi list
### To plot only a marker's annotation
### Plotting Bar Codes Using an AJ-510
### Setting Up Alteration Requirements
### Workflow for Alterations
### To create an alterations rule table
### To retrieve and edit an alterations rule table
### To create a size code table for alterations
### To order a marker with alterations
### Using Base Measurements
### Activity Log Screen
### Plot Options
### Block Fusing
### Overview of Block Fusing When Using a GERBERcutter
### Workflow for Block Fusing When Using a GERBERcutter
### Shell marker
### Fusing marker
### Block
### Block Fuse Amount
### Block Notch
### Canvas
### Create Fuse
### Cut Net Parts
### Fusible
### Message Stop
### Op–Stop
### Reduce Fuse Amount
### Shell
### Block fusing
### AutoMark
### To process an AutoMark job list
### AutoMark Editor Field Explanations
### AutoMark Menu Commands
### AutoMark Log
### Grade Rule Table Editor
### Edit Digitized Editor
### Piece Plot Parameter Table
### Piece Plot
### Inputting Pattern Pieces
### Digitizing
### Digitizing Menu
### Digitizing Menu Options
### Digitizing Cursor
### Digitizing Cursor Buttons
### To select items from the digitizing menu
### To prepare pieces for digitizing
### Placing a Piece on the Digitizing Table
### Descriptive Piece Data
- Information You Need for Every Piece
### Making Perimeter Notes
### Including Internals in Your Piece
### Defining Internals
### When to Use Internal Labels
### Converting/Importing
### Using PDS/Silhouette
### To digitize a basic closed piece
### To digitizing special point numbers
### To digitize from a nest
### To digitize a mirrored piece
### To digitize a copy piece
### To digitize angled notches
### To digitize an angled notch using a rule table
### To digitize an angled notch using a nested piece
### Plotting Angled Notches
### To digitize internals on your piece
### To digitize multiple grain lines
### To digitize large pieces
### To digitize 90 degree angles
### To digitize paste pieces
### When digitizing the parent piece
### When digitizing the paste piece
### Paste Pieces
### Follow-On Pieces
### Guidelines for placing a paste piece outside a parent's perimeter
### Guidelines for placing a paste piece inside a parent's perimeter
### To digitize a follow-on piece
### Generating Reports
- What Reports are Available?
- To generate a Splice Report
- To generate a Single Piece Report
- To generate an All Piece Report
- To generate a Piece Perimeter Report
- To generate an All Marker Report
- To generate an All Layrule Report
- To generate an All Plot Report
- To generate an All Cut Report
- Grading and Grade Rules
### How Grading Works in AccuMark
### Sample Graded Pattern
### Grade Rule Tables
### Things to Remember About Grading
### Naming a Grade Rule Table
### To create a grade rule table
### To retrieve and edit a grade rule table
### To search for a grade rule
### To display a specific grade rule
### To display a specific size break
### To copy a grade rule
### To import a grade rule from another rule table
### To import a grade rule from a piece
### To change the grade rule values in a specific column
### To clear the grade rule values in a specific column
### Rules
### Search
### Go To Rule
### Go To Size
### Copy Rule
### Import Rule
### Import PC–Rule
### Change Sign
### Clear Column
### What if I Can't Retrieve a Digitized Piece?
### Display Piece
### Display Graded
### To edit the grain line for a piece
### To edit the points in a piece
### To display a grade point
### Go To Point
### Next Point
### Insert Point
### To delete a point
### To change a point
### Delete an internal
### Button Types
### Edit Digitize Screen Menu Commands
### To edit digitized data
### To add a line to digitized data
### To delete a line from digitized data
### Piece Plotting
### Plotter Parameter Tables Versus Plotter Settings
### To plot pieces
### Perform Piece Plots by Model
### To save piece plot data as a DOS file
### Store Verifying
### Retrv Original
### Definitions:
### Sliding layrules
### Current storage area
### Default storage area
### Constructs
### Piece
### Digitized data
### Manual grading
### Wildcard
### Statically
### Segment
### Dynamically
### Internals
### Dead zone
### Nest
### Locator points
### Transition points
### Modular patterns
### Point Limits
### Digitizer Storage Location
### Current Storage Location
### Digitized data
### Bundle
### Model options
### Half piecing
### Dynamic piecing
### Model
### Match marks
### Full body measurement
### Blue pencil alteration amount
### Layrules
### Dry haul
### Heelcuts
### Overcuts
### Cutter configuration file
### Alternate grain line
### Getting Started
### Overview
### The AccuMark Marker Creation, Editors page of the GERBER LaunchPad provides the
### editors to create and customize AccuMark forms and parameter tables to meet your
### company’s specifications.
### Workflow for Ordering and Processing Markers
### The typical workflow for ordering and processing markers consists of the tasks shown
### below. This workflow assumes you have completed the initial setup requirements. Click
### on any task in the workflow shown below to learn more about that task.
### Note: Once a marker order is successfully processed, the marker can be retrieved in the
### Marker Making application, made (if needed), and stored. After being stored, the marker
### can then be plotted to check for accuracy. If you have a GERBERcutter, you can also
### generate cut data from the marker and plot the cut data to further check for accuracy.
### Using Order Entry
### Working with Storage Areas
### Storage Areas are user def

## IGES Translator (Import/Export)

### Export — IGESOUT.EXE (AccuMark piece → IGES format)
- Command: `IGESOUT [options] <storage_area> <piece_name> <IGES_filename>`
- `/?` or `/h` — display usage help
- `/U<u>` — override output units (1=Inches, 2=Millimeters, 10=Centimeters)

### Import/Convert — IGES.EXE (IGES format → AccuMark Raw Piece data)
- Command: `IGES <input-specification> <output-specification> [options]`
- `-A<n>` — Closure Amount: max gap (in 1/100 inch) allowed between adjacent lines to still close a perimeter
- `-T<d>` — Trimming: remove colinear points; optional `<d>` sets max endpoint distance for conditional trimming
- `-G` — Grade Points: assign a grade point to each new entity (from the IGES directory-section line number)
- `-MA<n>` — Arc Points: cap the number of points generated for an arc
- `-MB<n>` — Spline Points: cap the number of points generated for a b-spline
- `-I` — Pasting Internals: convert an open internal with endpoints on the perimeter into a notch
- `-L` — List data processing to screen (debugging)
- `-P` — List data processing to printer (debugging)
- `-D` — Drill Holes: convert IGES Point Entities to drill holes
- `-U<u>` — Override Unit: 1=Inches, 2=Millimeters, 3=Feet, 6=Meters, 10=Centimeters
- `-S` — Override Smoothing: assign Non-Smooth point attribute to every point
- `-O<storage_area>` — Online to AccuMark: write Raw Piece data directly into a named AccuMark Storage Area

### IGES.INI parameter file (persistent defaults, read automatically by IGES.EXE)
- `StorageAreaName=` — sets the AccuMark Storage Area, removing the need for `-O` on every call
- `PieceNameAtLine=` — which Start Section line holds the piece name (auto-extracted instead of typed)
- `DescriptionAtLine=` — which Start Section line holds the piece description
- `CategoryAtLine=` — which Start Section line holds the piece category

### Post-conversion — AccuMark IMPORT DATA editor (when not using `-O`)
- Select data type: DIGITIZE DATA
- Specify input directory and output storage area
- Process (`F1` or select PROCESS)
- Verify the piece (in Pattern Design)


## Style Converter

### Main workflow functions
- Select style(s) to convert (name or wildcard — wildcards recommended above ~2,000 styles)
- Inspection Options — dialog to enable auto-save of warning/error styles to folders (default `C:\ads`)
- Convert / Run
- Results dialog — summary + prompt to save flagged styles into the specified folders
- Report Results — opens the generated CSV (e.g. in Excel) of all warnings/errors
- Style Converter Viewer — overlay AccuMark vs. MicroMark versions of a piece
  - Measure function — measure the difference between the two overlaid shapes
  - Snap to Geometry — align the two versions for comparison

### Detected error conditions (each maps to a specific fix path)
- Intersection error while grading piece — fix perimeter/grade rules in PDS
- Piece modification has invalidated a corner angle — reapply/edit corner type in PDS
- Unable to store, 2 F points required — remove one Grain Line in MicroMark PDS before converting
- Failed MicroMark grading — run Update on styldir/gdrldir, check rule table
- Invalid matching lines — matching lines must be parallel/perpendicular to the G0/F line
- Rule Table missing — copy the rule table to `\ads\gdrldir`, or repoint the style to an existing table
- MicroMark sizes missing — remove or edit the referenced synonym table
- Missing OPP Grade Axis — define the OPP Grade Axis, in MicroMark or AccuMark
- Cannot find rule –1 — assign a valid rule number to the point in MicroMark PDS
- Sizes has variations and can not be converted (Grade Checker Error, not a Viewer mismatch —
  see manual "Grade Checker Error" section) — check the synonym table, convert it into a size
  code, and create the necessary alteration rules before re-converting

### Detected warning conditions
- Piece was flipped, grain line realigned to maintain flip state
- Piece with grain line converted to F Rotation will not rotate the same way in AM vs. MK marking
- Piece message has been truncated (32-char MicroMark field → 20-char AccuMark field)
- Cut lines are not present in MicroMark piece — sew perimeter used for comparison
- Unavailable rules converted to 0 growth
- Tangent rule not valid on points, replaced with 0 growth

### Detected mismatch conditions (Style Converter Viewer)
- Intersection Moved
- Curves Different
- Changes in Notches
- Overall Perimeter Changes (piece origin offset)
