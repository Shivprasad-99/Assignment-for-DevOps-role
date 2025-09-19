package main

import (
	"context"
	"fmt"
	"log"

	"github.com/aws/aws-sdk-go-v2/aws"
	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/s3"
)

func main() {
	// Load AWS configuration 
	cfg, err := config.LoadDefaultConfig(context.TODO())
	if err != nil {
		log.Fatalf("Unable to load AWS config, %v", err)
	}

	// Create an S3 client
	s3Client := s3.NewFromConfig(cfg)

	// Call ListBuckets API
	result, err := s3Client.ListBuckets(context.TODO(), &s3.ListBucketsInput{})
	if err != nil {
		log.Fatalf("Unable to list buckets, %v", err)
	}

	// Print all bucket names with creation dates
	fmt.Println("S3 Buckets:")
	for _, bucket := range result.Buckets {
		fmt.Printf(" - %s (created on %s)\n",
			aws.ToString(bucket.Name),
			bucket.CreationDate.Format("2006-01-02 15:04:05"))
	}
}
