import math
from datetime import datetime, timedelta
from pathlib import Path
import altair as alt

import pandas as pd
import streamlit as st

import math
from datetime import datetime, timedelta
from pathlib import Path
import altair as alt

import pandas as pd
import streamlit as st

st.set_page_config(layout="wide")

st.markdown(
    """
<div style="
    background: linear-gradient(135deg, #FFE5D9, #FFF8F2);
    padding: 25px;
    border-radius: 16px;
    text-align: center;
    margin-bottom: 20px;
">
    <h1 style="color:#C8553D;">👣 Move Math</h1>
    <p style="font-size:18px; color:#5C3A21;">
        Plan your steps. Structure your day. Finish strong.
    </p>
</div>
""",
    unsafe_allow_html=True,
)

st.image(
    "https://images.unsplash.com/photo-1506744038136-46273834b3fb",
    use_container_width=True,
)
st.html(
    """
<style>
/* ===== PAGE ===== */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 950px;
}

[data-testid="stAppViewContainer"] {
    background: linear-gradient(180deg, #FFF8F2 0%, #FFFDFB 100%);
}

/* ===== TOP BAR ===== */
[data-testid="stHeader"] {
    background-color: #FFF8F2 !important;
}

[data-testid="stHeader"] * {
    color: #5C3A21 !important;
}

/* ===== SIDEBAR ===== */
[data-testid="stSidebar"] {
    background-color: #FFF3E8 !important;
}

[data-testid="stSidebar"] * {
    color: #5C3A21 !important;
}

/* ===== TITLES ===== */
h1 {
    color: #C8553D !important;
    text-align: center;
    font-weight: 800 !important;
}

h2, h3 {
    color: #D97706 !important;
    font-weight: 700 !important;
}

/* ===== GENERAL TEXT ===== */
p, label, div, span {
    color: #5C3A21;
}

/* ===== METRICS ===== */
[data-testid="stMetric"] {
    background-color: #FFF7F0 !important;
    border: 1px solid #F4C7A1 !important;
    padding: 12px;
    border-radius: 14px;
}

[data-testid="stMetricValue"] {
    color: #C8553D !important;
    font-weight: 800 !important;
}

[data-testid="stMetricLabel"] {
    color: #7A4A2E !important;
    font-weight: 600 !important;
}

/* ===== BUTTONS ===== */
.stButton > button {
    background-color: #E76F51 !important;
    color: white !important;
    border-radius: 12px !important;
    border: none !important;
    font-weight: 700 !important;
}

.stButton > button:hover {
    background-color: #D65A3D !important;
}

/* ===== INPUTS ===== */
div[data-baseweb="input"] > div {
    background-color: #FFFDF9 !important;
    border: 1px solid #E7BFA7 !important;
    border-radius: 12px !important;
}

div[data-baseweb="input"] input {
    color: #5C3A21 !important;
}

/* ===== SELECT BOX ===== */
div[data-baseweb="select"] > div {
    background-color: #FFFDF9 !important;
    border: 1px solid #E7BFA7 !important;
    border-radius: 12px !important;
    color: #5C3A21 !important;
}

/* ===== RADIO BUTTONS ===== */
div[role="radiogroup"] label {
    color: #5C3A21 !important;
    font-weight: 600 !important;
}

/* ===== ALERTS ===== */
[data-testid="stAlertContainer"] {
    border-radius: 12px !important;
}

[data-testid="stAlertContainer"] * {
    color: #5C3A21 !important;
}

/* ===== DATAFRAME AREA ===== */
[data-testid="stDataFrame"] {
    background-color: #FFFDF9 !important;
    border: 1px solid #E7BFA7 !important;
    border-radius: 12px !important;
    overflow: hidden;
}

[data-testid="stDataFrame"] * {
    color: #5C3A21 !important;
}

[data-testid="stDataFrame"] thead tr th {
    background-color: #FFF3E8 !important;
    color: #7A4A2E !important;
}

/* ===== PROGRESS TEXT ===== */
strong {
    color: #7A4A2E !important;
}
</style>
"""
)

DATA_FILE = Path("step_history.csv")


def get_steps_per_minute(activity: str, custom_spm: int) -> int:
    rates = {
        "Regular walk": 100,
        "Brisk walk": 120,
        "Stairs": 150,
        "March in place": 110,
        "Custom": custom_spm,
    }
    return rates.get(activity, 100)


def get_message(progress_percent: float) -> str:
    if progress_percent >= 100:
        return "🎉 You did it. Goal complete. Keep this energy going."
    if progress_percent >= 85:
        return "🔥 You’re so close. One more push and you’re there."
    if progress_percent >= 60:
        return "💪 Strong progress. Your consistency is building something real."
    if progress_percent >= 40:
        return "✨ You’re in motion now. Stay steady and let it add up."
    if progress_percent >= 20:
        return "🌱 A real start matters more than perfection. Keep going."
    return "🌞 Begin where you are. Every step counts and momentum grows."


def load_history() -> pd.DataFrame:
    if DATA_FILE.exists():
        df = pd.read_csv(DATA_FILE)
        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"])
        return df
    return pd.DataFrame(
        columns=[
            "date",
            "goal_steps",
            "current_steps",
            "steps_remaining",
            "activity",
            "steps_per_minute",
            "minutes_needed",
            "hit_goal",
        ]
    )


def save_today_record(
    date_value: str,
    goal_steps: int,
    current_steps: int,
    steps_remaining: int,
    activity: str,
    steps_per_minute: int,
    minutes_needed: float,
    hit_goal: bool,
) -> None:
    df = load_history()

    new_row = pd.DataFrame(
        [
            {
                "date": date_value,
                "goal_steps": goal_steps,
                "current_steps": current_steps,
                "steps_remaining": steps_remaining,
                "activity": activity,
                "steps_per_minute": steps_per_minute,
                "minutes_needed": round(minutes_needed, 1),
                "hit_goal": hit_goal,
            }
        ]
    )

    if not df.empty and "date" in df.columns:
        df["date_str"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")
        df = df[df["date_str"] != date_value].drop(columns=["date_str"])

    updated = pd.concat([df, new_row], ignore_index=True)
    updated.to_csv(DATA_FILE, index=False)


def parse_time(time_str: str) -> datetime:
    return datetime.strptime(time_str.strip(), "%I:%M %p")


def build_step_schedule(
    start_time_str: str,
    end_time_str: str,
    focus_minutes: int,
    walk_minutes: int,
    steps_per_minute: int,
    steps_remaining: int,
):
    try:
        start_dt = parse_time(start_time_str)
        end_dt = parse_time(end_time_str)

        if end_dt <= start_dt:
            end_dt += timedelta(days=1)

        schedule = []
        current_time = start_dt
        total_planned_steps = 0

        while True:
            focus_end = current_time + timedelta(minutes=focus_minutes)
            walk_end = focus_end + timedelta(minutes=walk_minutes)

            if walk_end > end_dt:
                break

            walk_steps = walk_minutes * steps_per_minute
            total_planned_steps += walk_steps

            schedule.append(
                {
                    "study_start": current_time.strftime("%I:%M %p"),
                    "study_end": focus_end.strftime("%I:%M %p"),
                    "walk_start": focus_end.strftime("%I:%M %p"),
                    "walk_end": walk_end.strftime("%I:%M %p"),
                    "walk_steps": walk_steps,
                }
            )

            current_time = walk_end

        steps_left_after_plan = max(steps_remaining - total_planned_steps, 0)
        return schedule, total_planned_steps, steps_left_after_plan, None

    except ValueError:
        return None, None, None, "Please enter times like 1:35 PM"


def find_open_slots(tasks):
    parsed_tasks = []

    for task in tasks:
        start_dt = parse_time(task["start"])
        end_dt = parse_time(task["end"])

        if end_dt <= start_dt:
            end_dt += timedelta(days=1)

        parsed_tasks.append(
            {"task_name": task["task_name"], "start_dt": start_dt, "end_dt": end_dt}
        )

    parsed_tasks = sorted(parsed_tasks, key=lambda x: x["start_dt"])

    open_slots = []
    for i in range(len(parsed_tasks) - 1):
        current_end = parsed_tasks[i]["end_dt"]
        next_start = parsed_tasks[i + 1]["start_dt"]

        if next_start > current_end:
            open_slots.append(
                {
                    "slot_start": current_end,
                    "slot_end": next_start,
                    "minutes_available": (next_start - current_end).total_seconds()
                    / 60,
                }
            )

    return parsed_tasks, open_slots


def build_plan_from_tasks(tasks, steps_remaining, steps_per_minute, min_walk_block=5):
    parsed_tasks, open_slots = find_open_slots(tasks)

    walk_plan = []
    total_planned_steps = 0

    for slot in open_slots:
        available_minutes = int(slot["minutes_available"])

        if available_minutes >= min_walk_block:
            walk_minutes = available_minutes
            walk_steps = walk_minutes * steps_per_minute

            walk_plan.append(
                {
                    "walk_start": slot["slot_start"].strftime("%I:%M %p"),
                    "walk_end": slot["slot_end"].strftime("%I:%M %p"),
                    "walk_minutes": walk_minutes,
                    "walk_steps": walk_steps,
                }
            )

            total_planned_steps += walk_steps

            if total_planned_steps >= steps_remaining:
                break

    steps_left_after_plan = max(steps_remaining - total_planned_steps, 0)
    extra_minutes_needed = (
        steps_left_after_plan / steps_per_minute if steps_per_minute > 0 else 0
    )

    return (
        parsed_tasks,
        open_slots,
        walk_plan,
        total_planned_steps,
        steps_left_after_plan,
        extra_minutes_needed,
    )


# 👇 THEN: your styling (THIS is where it goes)
st.markdown(
    """
<style>
footer {visibility: hidden;}
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
</style>
""",
    unsafe_allow_html=True,
)


# st.title("👣 Move Math")
st.caption("Track your movement. Finish your goal.")

st.subheader("Choose your goal")

goal_option = st.radio(
    "Pick a goal", ["6000", "8000", "10000", "Custom"], index=0, horizontal=True
)


activity = st.selectbox(
    "Activity type",
    ["Regular walk", "Brisk walk", "Stairs", "March in place", "Custom"],
)

st.subheader("Your inputs")

if goal_option == "Custom":
    custom_goal_text = st.text_input("Custom goal steps", value="7000")
    try:
        goal_steps = int(custom_goal_text)
        if goal_steps < 1000:
            goal_steps = 1000
        elif goal_steps > 50000:
            goal_steps = 50000
    except ValueError:
        st.warning("Please enter a whole number for custom goal steps.")
        goal_steps = 7000
else:
    goal_steps = int(goal_option)

current_steps_text = st.text_input("Current steps", value="1500")
try:
    current_steps = int(current_steps_text)
    if current_steps < 0:
        current_steps = 0
    elif current_steps > 100000:
        current_steps = 100000
except ValueError:
    st.warning("Please enter a whole number for current steps.")
    current_steps = 1500

custom_spm = 100
if activity == "Custom":
    custom_spm_text = st.text_input("Your steps per minute", value="100")
    try:
        custom_spm = int(custom_spm_text)
        if custom_spm < 1:
            custom_spm = 1
        elif custom_spm > 300:
            custom_spm = 300
    except ValueError:
        st.warning("Please enter a whole number for steps per minute.")
        custom_spm = 100

steps_per_minute = get_steps_per_minute(activity, custom_spm)

steps_remaining = max(goal_steps - current_steps, 0)
progress_percent = (current_steps / goal_steps) * 100 if goal_steps > 0 else 0
progress_decimal = min(progress_percent / 100, 1.0)
minutes_needed = steps_remaining / steps_per_minute if steps_per_minute > 0 else 0
rounded_minutes = math.ceil(minutes_needed)
finish_time = datetime.now() + timedelta(minutes=rounded_minutes)
today_str = datetime.now().strftime("%Y-%m-%d")

col1, col2, col3 = st.columns(3)
col1.metric("Goal", f"{goal_steps:,}")
col2.metric("Current", f"{current_steps:,}")
col3.metric("Remaining", f"{steps_remaining:,}")

st.progress(progress_decimal)
st.write(f"**Progress:** {progress_percent:.1f}%")

if "celebrate_clicked" not in st.session_state:
    st.session_state.celebrate_clicked = False

if "goal_celebrated" not in st.session_state:
    st.session_state.goal_celebrated = False

if steps_remaining == 0:
    st.success("🎉 Goal reached. Amazing work today.")

    if not st.session_state.goal_celebrated:
        st.balloons()
        st.session_state.goal_celebrated = True

    st.caption("Tap play for your celebration sound.")
    st.audio("success.mp3")
else:
    st.session_state.goal_celebrated = False
    st.info(get_message(progress_percent))

if steps_remaining == 0:
    st.success("🎉🎯You Did That!!! Celebrate!!!")
    st.balloons()
else:
    st.subheader("🎯 Your finish plan")
    st.write(f"**Activity selected:** {activity}")
    st.write(f"**Estimated pace:** {steps_per_minute} steps/min")
    st.write(f"**Minutes needed:** {minutes_needed:.1f}")
    st.write(f"**Finish around:** {finish_time.strftime('%I:%M %p')}")

activities = {"🚶 Walk": 100, "⚡ Brisk walk": 130, "🧗 Stair climb": 180}

st.subheader("Compare movement options")

regular_minutes = steps_remaining / 100 if steps_remaining > 0 else 0
brisk_minutes = steps_remaining / 120 if steps_remaining > 0 else 0
stairs_minutes = steps_remaining / 150 if steps_remaining > 0 else 0
march_minutes = steps_remaining / 110 if steps_remaining > 0 else 0

comp1, comp2 = st.columns(2)
with comp1:
    st.write(f"🚶 Regular walk: **{regular_minutes:.1f} min**")
    st.write(f"⚡ Brisk walk: **{brisk_minutes:.1f} min**")
with comp2:
    st.write(f"🧗 Stairs: **{stairs_minutes:.1f} min**")
    st.write(f"🎵 March in place: **{march_minutes:.1f} min**")
st.write("🧗 Stair climb (fastest way to finish)")
st.subheader("Quick challenge")
if steps_remaining > 0:
    if st.button("Give me a simple plan"):
        if steps_remaining <= 800:
            st.write("Try one 8-minute walk or 5–6 minutes of stairs.")
        elif steps_remaining <= 1500:
            st.write("Try one 12–15 minute walk, or split it into two short walks.")
        elif steps_remaining <= 3000:
            st.write("Try two 15-minute walks, or one brisk 20–25 minute session.")
        else:
            st.write("Try three short walks today or one longer movement session.")
else:
    st.write("Goal reached. Stretch, recover, and come back strong tomorrow.")

st.subheader("Can I finish by a certain time?")

target_time_str = st.text_input("Enter target time (example: 6:30 PM)", value="6:30 PM")

if steps_remaining > 0 and target_time_str:
    try:
        parsed_target = parse_time(target_time_str)
        now = datetime.now()

        target_today = now.replace(
            hour=parsed_target.hour,
            minute=parsed_target.minute,
            second=0,
            microsecond=0,
        )

        if target_today < now:
            target_today += timedelta(days=1)

        minutes_available = (target_today - now).total_seconds() / 60

        if minutes_available <= 0:
            st.warning("That target time has already passed.")
        else:
            needed_spm = steps_remaining / minutes_available
            st.write(f"**Minutes available:** {minutes_available:.1f}")
            st.write(f"**Steps per minute needed:** {needed_spm:.1f}")

            if needed_spm <= 100:
                st.success("That pace is very doable with a regular walk.")
            elif needed_spm <= 120:
                st.info("You’ll likely need a brisk walk to hit that target.")
            elif needed_spm <= 150:
                st.warning("You may need stairs or very steady movement to make it.")
            else:
                st.error("That target is tight — try giving yourself more time.")
    except ValueError:
        st.warning("Please enter time like 6:30 PM")

st.subheader("Auto-plan my day")

plan_col1, plan_col2 = st.columns(2)

with plan_col1:
    start_time_str = st.text_input("Start time", value="1:35 PM", key="auto_start_time")
    focus_minutes = st.number_input(
        "Focus block (minutes)", min_value=10, max_value=180, value=50, step=5
    )

with plan_col2:
    end_time_str = st.text_input("End time", value="6:00 PM", key="auto_end_time")
    walk_minutes = st.number_input(
        "Walk break (minutes)", min_value=1, max_value=60, value=10, step=1
    )

if st.button("Build my schedule"):
    schedule, total_planned_steps, steps_left_after_plan, error = build_step_schedule(
        start_time_str=start_time_str,
        end_time_str=end_time_str,
        focus_minutes=focus_minutes,
        walk_minutes=walk_minutes,
        steps_per_minute=steps_per_minute,
        steps_remaining=steps_remaining,
    )

    if error:
        st.warning(error)
    else:
        if not schedule:
            st.warning(
                "Not enough time blocks fit in that window. Try shorter focus blocks or a later end time."
            )
        else:
            st.success(f"Your plan could add about {total_planned_steps:,} steps.")

            for i, block in enumerate(schedule, start=1):
                st.write(
                    f"**Block {i}:** Study {block['study_start']}–{block['study_end']} | "
                    f"Walk {block['walk_start']}–{block['walk_end']} "
                    f"(~{block['walk_steps']:,} steps)"
                )

            if steps_left_after_plan > 0:
                extra_minutes = steps_left_after_plan / steps_per_minute
                st.info(
                    f"You would still need about {steps_left_after_plan:,} more steps "
                    f"({extra_minutes:.1f} extra minutes of movement)."
                )
            else:
                st.balloons()
                st.success(
                    "This plan should get you to your goal within your schedule."
                )

st.subheader("Plan my steps around my day")
st.write("Add up to 5 tasks and let the app find walking windows between them.")

num_tasks = st.number_input(
    "How many tasks do you want to enter?", min_value=1, max_value=5, value=3, step=1
)

tasks = []

default_tasks = [
    ("Study", "1:35 PM", "2:25 PM"),
    ("Dinner", "5:30 PM", "6:00 PM"),
    ("Bills", "6:15 PM", "6:45 PM"),
    ("Task 4", "7:00 PM", "7:30 PM"),
    ("Task 5", "8:00 PM", "8:30 PM"),
]

for i in range(int(num_tasks)):
    st.markdown(f"### Task {i+1}")

    col1, col2, col3 = st.columns(3)
    default_name, default_start, default_end = default_tasks[i]

    with col1:
        task_name = st.text_input(
            f"Task name {i+1}", value=default_name, key=f"task_name_{i}"
        )

    with col2:
        start_time = st.text_input(
            f"Start time {i+1}", value=default_start, key=f"task_start_{i}"
        )

    with col3:
        end_time = st.text_input(
            f"End time {i+1}", value=default_end, key=f"task_end_{i}"
        )

    tasks.append({"task_name": task_name, "start": start_time, "end": end_time})

min_walk_block = st.number_input(
    "Minimum walk block to count (minutes)",
    min_value=1,
    max_value=60,
    value=5,
    step=1,
    key="min_walk_block",
)

if st.button("Build plan around my tasks"):
    try:
        (
            parsed_tasks,
            open_slots,
            walk_plan,
            total_planned_steps,
            steps_left_after_plan,
            extra_minutes_needed,
        ) = build_plan_from_tasks(
            tasks=tasks,
            steps_remaining=steps_remaining,
            steps_per_minute=steps_per_minute,
            min_walk_block=min_walk_block,
        )

        st.markdown("## Your tasks")
        for task in parsed_tasks:
            st.write(
                f"**{task['task_name']}**: "
                f"{task['start_dt'].strftime('%I:%M %p')}–{task['end_dt'].strftime('%I:%M %p')}"
            )

        st.markdown("## Open walking windows")
        if not open_slots:
            st.warning("No open time slots found between your tasks.")
        else:
            for slot in open_slots:
                st.write(
                    f"Open slot: **{slot['slot_start'].strftime('%I:%M %p')}–{slot['slot_end'].strftime('%I:%M %p')}** "
                    f"({slot['minutes_available']:.0f} min available)"
                )

        st.markdown("## Suggested walking plan")
        if not walk_plan:
            st.warning("No walking blocks fit your settings.")
        else:
            for i, walk in enumerate(walk_plan, start=1):
                st.write(
                    f"**Walk {i}:** {walk['walk_start']}–{walk['walk_end']} "
                    f"({walk['walk_minutes']} min, about {walk['walk_steps']:,} steps)"
                )

        st.metric("Planned steps", f"{total_planned_steps:,}")

        if steps_left_after_plan > 0:
            st.info(
                f"You would still need about **{steps_left_after_plan:,}** more steps "
                f"({extra_minutes_needed:.1f} more minutes of movement)."
            )
        else:
            st.success("This plan should get you to your goal.")
            st.balloons()

    except ValueError:
        st.error("Please enter all times like 1:35 PM or 6:00 PM.")

st.subheader("Save today")

if st.button("Save Today’s Progress"):
    save_today_record(
        date_value=today_str,
        goal_steps=goal_steps,
        current_steps=current_steps,
        steps_remaining=steps_remaining,
        activity=activity,
        steps_per_minute=steps_per_minute,
        minutes_needed=minutes_needed,
        hit_goal=(steps_remaining == 0),
    )
    st.success("Today’s progress saved.")

history_df = load_history()

st.subheader("Recent history")

streak = 0

if history_df.empty:
    st.write("No saved history yet. Save today’s progress to start tracking.")
else:
    history_df = history_df.sort_values("date")
    history_df["date"] = pd.to_datetime(history_df["date"])

    chart_df = history_df.copy()[["date", "current_steps", "goal_steps"]]

    chart = (
        alt.Chart(chart_df)
        .transform_fold(["current_steps", "goal_steps"], as_=["metric", "steps"])
        .mark_line(point=True)
        .encode(
            x=alt.X("date:T", title="Date"),
            y=alt.Y("steps:Q", title="Steps"),
            color=alt.Color(
                "metric:N",
                scale=alt.Scale(
                    domain=["current_steps", "goal_steps"], range=["#E76F51", "#F4A261"]
                ),
                legend=alt.Legend(title="Metric"),
            ),
        )
        .properties(height=350)
        .configure(background="#FFFDF9")
        .configure_axis(labelColor="#5C3A21", titleColor="#5C3A21", gridColor="#E7BFA7")
        .configure_legend(labelColor="#5C3A21", titleColor="#5C3A21")
    )

    st.altair_chart(chart, width="stretch")

    display_df = history_df.sort_values("date", ascending=False).copy()
    display_df["date"] = display_df["date"].dt.strftime("%Y-%m-%d")

    st.table(
        display_df[
            [
                "date",
                "current_steps",
                "goal_steps",
                "steps_remaining",
                "activity",
                "minutes_needed",
                "hit_goal",
            ]
        ]
    )

    hits = history_df.sort_values("date")["hit_goal"].tolist()
    streak = 0
    for val in reversed(hits):
        if bool(val):
            streak += 1
        else:
            break

    st.metric("Current goal streak", f"{streak} day(s)")

    if streak >= 3:
        st.success("🔥 You're building momentum. Keep going.")
    if streak >= 7:
        st.balloons()
        st.success("🌟 7 day streak! This is becoming a real habit.")
