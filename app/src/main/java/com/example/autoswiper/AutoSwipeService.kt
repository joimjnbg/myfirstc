package com.example.autoswiper

import android.accessibilityservice.AccessibilityService
import android.accessibilityservice.GestureDescription
import android.graphics.Path
import android.os.Handler
import android.os.Looper
import android.view.accessibility.AccessibilityEvent
import kotlin.random.Random

class AutoSwipeService : AccessibilityService() {

    private val swipeHandler = Handler(Looper.getMainLooper())
    private lateinit var swipeRunnable: Runnable

    private val doubleClickHandler = Handler(Looper.getMainLooper())
    private lateinit var doubleClickRunnable: Runnable

    companion object {
        var isRunning = false
    }

    override fun onServiceConnected() {
        super.onServiceConnected()
        startSwipingLoop()
        startDoubleClickLoop()
    }

    private fun startSwipingLoop() {
        swipeRunnable = object : Runnable {
            override fun run() {
                if (isRunning) {
                    performSwipe()
                }
                val delay = if(isRunning) Random.nextLong(1000, 60000) else 500
                swipeHandler.postDelayed(this, delay)
            }
        }
        swipeHandler.post(swipeRunnable)
    }

    private fun startDoubleClickLoop() {
        doubleClickRunnable = object : Runnable {
            override fun run() {
                if (isRunning) {
                    performDoubleClick()
                }
                val delay = if(isRunning) Random.nextLong(30000, 300000) else 500
                doubleClickHandler.postDelayed(this, delay)
            }
        }
        doubleClickHandler.post(doubleClickRunnable)
    }

    private fun performSwipe() {
        val displayMetrics = resources.displayMetrics
        val width = displayMetrics.widthPixels
        val height = displayMetrics.heightPixels
        val marginX = (width * 0.1).toInt()
        val marginY = (height * 0.1).toInt()
        val path = Path()
        val swipeUp = Random.nextInt(0, 10) >= 1

        if (swipeUp) {
            val startX = Random.nextInt(marginX, width - marginX)
            val startY = Random.nextInt(height / 2, height - marginY)
            val endY = (startY - Random.nextInt((height * 0.2).toInt(), (height * 0.3).toInt())).coerceAtLeast(marginY)
            path.moveTo(startX.toFloat(), startY.toFloat())
            path.lineTo(startX.toFloat(), endY.toFloat())
        } else {
            val startX = Random.nextInt(marginX, width - marginX)
            val startY = Random.nextInt(marginY, height / 2)
            val endY = (startY + Random.nextInt((height * 0.2).toInt(), (height * 0.3).toInt())).coerceAtMost(height - marginY)
            path.moveTo(startX.toFloat(), startY.toFloat())
            path.lineTo(startX.toFloat(), endY.toFloat())
        }
        val gesture = GestureDescription.Builder().addStroke(GestureDescription.StrokeDescription(path, 0, 200)).build()
        dispatchGesture(gesture, null, null)
    }

    private fun performDoubleClick() {
        val displayMetrics = resources.displayMetrics
        val width = displayMetrics.widthPixels
        val height = displayMetrics.heightPixels

        val clickX = Random.nextInt(width / 4, width * 3 / 4).toFloat()
        val clickY = Random.nextInt(height / 4, height * 3 / 4).toFloat()

        val path = Path().apply { moveTo(clickX, clickY) }

        val gesture = GestureDescription.Builder()
            .addStroke(GestureDescription.StrokeDescription(path, 0, 50))
            .addStroke(GestureDescription.StrokeDescription(path, 150, 50))
            .build()
        dispatchGesture(gesture, null, null)
    }

    override fun onAccessibilityEvent(event: AccessibilityEvent?) {}

    override fun onInterrupt() {}

    override fun onDestroy() {
        super.onDestroy()
        swipeHandler.removeCallbacks(swipeRunnable)
        doubleClickHandler.removeCallbacks(doubleClickRunnable)
        isRunning = false
    }
}