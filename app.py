import streamlit as st
import mysql.connector

# Connect to the MySQL database
db = mysql.connector.connect(
    host="localhost",  # The hostname of your MySQL server (use your XAMPP server address)
    user='root',  # Your MySQL username
    password='',  # Your MySQL password
    database="yoga_dictionary"  # Your MySQL database name
)

cursor = db.cursor()

# Streamlit UI
st.title("Yoga Poses App")

# Sidebar Dashboard
st.sidebar.title("Dashboard")
cursor.execute("SELECT * FROM yoga_poses")
poses = cursor.fetchall()
selected_option = st.sidebar.selectbox("Select an Action", ["Search", "Add", "Update", "Delete"])

if selected_option == "Search":
    st.sidebar.subheader("Search Yoga Poses")
    search_query = st.sidebar.text_input("Enter a search term")
    if st.sidebar.button("Search"):
        cursor.execute("SELECT * FROM yoga_poses WHERE name LIKE %s OR description LIKE %s OR tag LIKE %s", (f"%{search_query}%", f"%{search_query}%", f"%{search_query}%"))
        found_poses = cursor.fetchall()

        if found_poses:
            st.subheader("Search Results")
            for pose in found_poses:
                st.write(f"Name: {pose[1]}")
                st.write(f"Description: {pose[2]}")
                st.write(f"Benefits: {pose[4]}")
                st.image(pose[3], use_column_width=True)
        else:
            st.warning("No matching yoga poses found.")

if selected_option == "Add":
    st.sidebar.subheader("Add a New Yoga Pose")
    name = st.sidebar.text_input("Name")
    description = st.sidebar.text_area("Description")
    image_url = st.sidebar.text_input("Image URL")
    benefits = st.sidebar.text_area("Benefits")
    tag = st.sidebar.text_input("Tags (comma-separated)")

    if st.sidebar.button("Add"):
        # Insert data into the yoga_poses table, including the new "tag" column
        cursor.execute("INSERT INTO yoga_poses (name, description, image_url, benefits, tag) VALUES (%s, %s, %s, %s, %s)", (name, description, image_url, benefits, tag))
        db.commit()
        st.success("Pose added successfully!")


if selected_option == "Update":
    st.sidebar.subheader("Update a Yoga Pose")
    pose_to_update = st.sidebar.selectbox("Select a Pose to Update", [pose[1] for pose in poses])

    # Get the selected pose details
    selected_pose = [pose for pose in poses if pose[1] == pose_to_update][0]

    st.sidebar.subheader("Update Pose Details")
    updated_name = st.sidebar.text_input("Name", value=selected_pose[1])
    updated_description = st.sidebar.text_area("Description", value=selected_pose[2])
    updated_image_url = st.sidebar.text_input("Image URL", value=selected_pose[3])
    updated_benefits = st.sidebar.text_area("Benefits", value=selected_pose[4])

    if st.sidebar.button("Update"):
        # Update all columns for the selected pose
        cursor.execute("UPDATE yoga_poses SET name = %s, description = %s, image_url = %s, benefits = %s WHERE name = %s",
                       (updated_name, updated_description, updated_image_url, updated_benefits, pose_to_update))
        db.commit()
        st.success("Pose updated successfully!")


if selected_option == "Delete":
    st.sidebar.subheader("Delete a Yoga Pose")
    pose_to_delete = st.sidebar.selectbox("Select a Pose to Delete", [pose[1] for pose in poses])
    if st.sidebar.button("Delete"):
        cursor.execute("DELETE FROM yoga_poses WHERE name = %s", (pose_to_delete,))
        db.commit()
        st.warning(f"{pose_to_delete} deleted!")

# Read
# st.header("Yoga Poses")
cursor.execute("SELECT * FROM yoga_poses")
poses = cursor.fetchall()
for pose in poses:
    st.header(f"{pose[1]}")
    st.image(pose[3], use_column_width=True)
    st.write(f"{pose[2]}")
    st.write(f"Benefits: {pose[4]}")

# Close the database connection
db.close()