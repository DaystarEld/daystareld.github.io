# How to Copy WordPress Images

## The Situation

WordPress creates multiple versions of each image (thumbnails, different sizes) and stores them in date-based folders. That's why you're seeing dozens of copies - they're different sizes of the same image.

## What You Need to Copy

I've identified **32 missing images** that your site actually uses. Here's the organized list:

### From 2012/09/
- `choice-300x254.jpg` (or `choice.jpg` - full size version)

### From 2013/01/
- `81tObD4f10L._AA1500_-300x300.jpg`

### From 2013/02/
- `The_Tavern-300x154.jpg` (or `The_Tavern.jpg`)
- `chronotrigger-300x180.jpg` (or `chronotrigger.jpg`)
- `night_of_the_fortress_castle_marina_water_lightning_fires-1920x1080-300x168.jpg` (or full size)
- `railroading.gif`

### From 2013/03/
- `padbirth-fuckyeahpadmeamidala-300x127.png` (or `padbirth-fuckyeahpadmeamidala.png`)
- `rope-tension.jpg`

### From 2013/04/
- `calvin_arguing-300x202.png` (or `calvin_arguing.png`)
- `jlh-supwall-300x225.jpg` (or `jlh-supwall.jpg`)
- `retard-owl-300x98.jpg` (or `retard-owl.jpg`)

### From 2017/03/
- `Eclipse-300x195.jpg` (or `Eclipse.jpg`)
- `Eclipse-Rise-217x300.jpg` (or `Eclipse-Rise.jpg`)

### From 2020/09/
- `Behaviorist.png`
- `Existential-2.png`
- `Systemic-1.png`

### From 2020/10/
- `Psychoanalytic.png`

### From 2022/01/
- `Cat-Dinner-300x230.jpg` (or `Cat-Dinner.jpg`)
- `Steph-and-I-300x300.jpg` (or `Steph-and-I.jpg`)

### From 2022/02/
- `ACTR5-1024x512.jpg` (or `ACTR5.jpg`)

### From 2022/10/
- `Scarfy.jpg`

### From 2023/01/
- `Vuln.png`

### From 2023/02/
- `Stress.png`

### From 2023/03/
- `23Me.png`

## Easy Copy Method

### Option 1: Copy the Entire Month Folders (Recommended)

Since WordPress organizes by year/month, just copy these entire folders from your GoDaddy WordPress:

```
wp-content/uploads/2012/09/  → Copy to your repo
wp-content/uploads/2013/01/  → Copy to your repo
wp-content/uploads/2013/02/  → Copy to your repo
wp-content/uploads/2013/03/  → Copy to your repo
wp-content/uploads/2013/04/  → Copy to your repo
wp-content/uploads/2017/03/  → Copy to your repo
wp-content/uploads/2020/09/  → Copy to your repo
wp-content/uploads/2020/10/  → Copy to your repo
wp-content/uploads/2022/01/  → Copy to your repo
wp-content/uploads/2022/02/  → Copy to your repo
wp-content/uploads/2022/10/  → Copy to your repo
wp-content/uploads/2023/01/  → Copy to your repo
wp-content/uploads/2023/02/  → Copy to your repo
wp-content/uploads/2023/03/  → Copy to your repo
```

This will copy all versions of the images, but that's fine - it ensures you get the right sizes.

### Option 2: Copy Individual Files

If you want to be selective, look for the filenames above in each month folder.

**Pro tip:** When you see multiple versions like:
- `image.jpg` (original full size)
- `image-300x200.jpg` (medium)
- `image-150x150.jpg` (thumbnail)

Copy the FULL SIZE version if available (the one without dimensions in the name), or the largest version you can find.

## Where to Copy Them

Copy the entire folder structure to your repo:

```
C:\Users\dayst\Documents\Daystar\Website\daystareld.github.io\wp-content\uploads\
```

The folder structure should mirror what's on GoDaddy:
```
wp-content/
  uploads/
    2012/
      09/
        choice.jpg
    2013/
      01/
        ...
    etc.
```

## After Copying

Once you've copied the images:

1. Run this to check what's still missing:
   ```
   python scripts/find_missing_images.py
   ```

2. Test locally:
   ```
   python -m http.server 8000
   ```
   Visit affected pages to see if images load

3. Commit and push:
   ```
   git add wp-content/
   git commit -m "Add missing WordPress images"
   git push origin main
   ```

## If Images Are Still Missing

If you can't find some images on GoDaddy, they might have been:
- Deleted from WordPress before export
- External links (already handled)
- Can be replaced with new images or removed

Let me know when you've copied the folders and I'll help verify everything works!

