# Missing Images Report

## Summary

**36 images** are referenced in blog posts but missing from the repository. These were hosted on the WordPress site at `daystareld.com/wp-content/uploads/`.

## Missing Images by Post

### Blog Posts Missing Images:

1. **blog/date-me** (1 image)
   - `/wp-content/uploads/2022/10/Scarfy.jpg`

2. **blog/dating-testimonials** (2 images)
   - `/wp-content/uploads/2022/01/Steph-and-I-300x300.jpg`
   - `/wp-content/uploads/2022/01/Cat-Dinner-300x230.jpg`

3. **blog/eclipse-review** (1 image)
   - `/wp-content/uploads/2017/03/Eclipse-300x195.jpg`

4. **blog/eclipse-review-2** (1 image)
   - `/wp-content/uploads/2017/03/Eclipse-Rise-217x300.jpg`

5. **blog/emotions-make-sense** (2 images)
   - `/wp-content/uploads/2025/08/Emotions.png` (featured image - already added from external URL)
   - `/wp-content/uploads/2022/03/5-Minutes.jpg` (inline)

6. **blog/executive-dysfunction-101** (1 image)
   - `/wp-content/uploads/2022/07/PEF-0.png`

7. **blog/executive-function-1** (1 image)
   - `/wp-content/uploads/2022/07/PEF-1.png`

8. **blog/executive-function-2** (3 images)
   - `/wp-content/uploads/2022/07/PEF-2.png`
   - `/wp-content/uploads/2023/05/Self-Reflection.png`
   - `/wp-content/uploads/2023/05/Summon-Sapience.png`

9. **blog/executive-function-3** (6 images)
   - `/wp-content/uploads/2022/07/PEF-3.png`
   - `/wp-content/uploads/2024/05/Spreadsheet.png`
   - `/wp-content/uploads/2024/05/Kanban.png`
   - `/wp-content/uploads/2024/05/Hats.png`
   - `/wp-content/uploads/2024/05/TRIZ.png`
   - `/wp-content/uploads/2024/05/Color-Penta.png`

10. **blog/game-of-thrones-game-review** (2 images)
    - `/wp-content/uploads/2016/04/GoT-Game-300x300.jpg`
    - `/wp-content/uploads/2016/04/GoT-300x225.jpg`

11. **blog/philosophy-of-therapy** (1 image)
    - `/wp-content/uploads/2020/09/Therapies-Venn-2-2.png`

12. **blog/review-100-years** (1 image)
    - `/wp-content/uploads/2018/02/100years-296x300.jpg`

13. **blog/review-cultists-of-cthulhu** (1 image)
    - `/wp-content/uploads/2017/03/Cultists-224x300.jpg`

14. **blog/review-dance-with-dragons-expansion** (6 images)
    - `/wp-content/uploads/2016/04/Tullys-e1460093999970-286x300.jpg`
    - `/wp-content/uploads/2016/04/Freys-300x238.png`
    - `/wp-content/uploads/2016/04/Boltons-e1460094058925-286x300.jpg`
    - `/wp-content/uploads/2016/04/Mormonts-e1460094113959-300x284.jpg`
    - `/wp-content/uploads/2016/04/Arryns-285x300.jpg`
    - `/wp-content/uploads/2016/04/Stormlands-266x300.jpg`

15. **blog/sample-page** (1 image)
    - `/wp-content/uploads/2022/03/ParkingTicket.jpg`

16. **blog/secure-attachment** (1 image)
    - `/wp-content/uploads/2022/03/Secure-Attachment.png`

17. **blog/some-things-i-can-teach** (1 image)
    - `/wp-content/uploads/2022/03/LessWrong-Logo.png`

18. **blog/spec-ops-review** (1 image)
    - `/wp-content/uploads/2017/03/Spec-Ops-300x140.jpg`

19. **blog/stormlight-archives** (1 image)
    - `/wp-content/uploads/2018/02/Stormlight-292x300.jpg`

20. **blog/the-last-jedi-review** (1 image)
    - `/wp-content/uploads/2018/01/LastJedi-300x169.jpg`

21. **blog/therapy-vs-coaching** (1 image)
    - `/wp-content/uploads/2022/02/Therapist-or-Coach.png`

## Solutions

### Option 1: Download from Live WordPress Site (If Still Up)

If your WordPress site is still accessible at `daystareld.com`, I can create a script to download all these images automatically.

### Option 2: Download from WordPress Export/Backup

If you have a WordPress backup that includes media files, we can extract them from there.

### Option 3: Manual Download

You can manually download each image from your WordPress site's media library and place them in the correct directory structure:

```
wp-content/
  uploads/
    2016/04/
    2017/03/
    2018/01/
    2018/02/
    2020/09/
    2022/01/
    2022/02/
    2022/03/
    2022/07/
    2022/10/
    2023/05/
    2024/05/
    2025/08/
```

### Option 4: Update Image URLs

We could update the HTML to point to external URLs (if the images are hosted elsewhere) or use placeholder images.

## Next Steps

1. Let me know if the WordPress site is still accessible
2. If yes, I can create a download script
3. If no, we'll need to find another source for these images
4. Alternatively, we can replace them with new images or remove them

