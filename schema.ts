import {
    bool,
    itemType,
    string,
    timestampSeconds,
    uint,
  } from "@stately-cloud/schema";

  /**
   * Link item type definition for the link tracker application.
   * Represents a trackable link associated with a user profile.
   */
  itemType("Link", {
    keyPath: "/p-:profileId/l-:id",
    fields: {
      /** Unique identifier for the link (auto-generated sequence) */
      id: { type: uint, required: false, initialValue: "sequence" },
      /** ID of the profile that owns this link */
      profileId: { type: string },
      /** Display title for the link */
      title: { type: string },
      /** Target URL that the link points to */
      url: { type: string },
      /** Emoji icon associated with the link */
      emoji: { type: string },
      /** Category or type classification of the link */
      linkType: { type: string },
      /** Optional description text for the link */
      description: { type: string },
      /** Whether the link is currently active/visible */
      isActive: { type: bool, required: false },
      /** Display order position for the link */
      order: { type: uint },
      /** Number of times this link has been clicked */
      clickCount: { type: uint },
      /** Timestamp when the link was created */
      createdAt: {
        type: timestampSeconds,
        required: false,
        fromMetadata: "createdAtTime",
      },
      /** Timestamp when the link was last updated */
      updatedAt: {
        type: timestampSeconds,
        required: false,
        fromMetadata: "lastModifiedAtTime",
      },
    },
  });

  /**
   * Profile item type definition for user profiles.
   * Represents a user's public profile page containing their links.
   */
  itemType("Profile", {
    keyPath: "/p-:id",
    fields: {
      /** Unique identifier for the profile */
      id: { type: string },
      /** User's full display name */
      fullName: { type: string },
      /** URL-friendly slug for the profile */
      slug: { type: string },
      /** URL to the user's profile image */
      profileImage: { type: string },
      /** User's biography or description text */
      bio: { type: string },
      /** Whether the profile is currently active/visible */
      isActive: { type: bool, required: false },
      /** Timestamp when the profile was created */
      createdAt: {
        type: timestampSeconds,
        required: false,
        fromMetadata: "createdAtTime",
      },
      /** Timestamp when the profile was last updated */
      updatedAt: {
        type: timestampSeconds,
        required: false,
        fromMetadata: "lastModifiedAtTime",
      },
      /** Number of times this profile has been viewed */
      viewCount: { type: uint },
    },
  });